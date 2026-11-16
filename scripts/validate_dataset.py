#!/usr/bin/env python3
"""Fail-closed schema, provenance, unit, chronology and quarantine checks."""
import csv,datetime as dt,hashlib,json,math,re
from decimal import Decimal
from pathlib import Path
from schema import SCHEMAS
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'glif_investment_dataset'
CHECKS=[]
def check(condition,message):
    if not condition:raise AssertionError(message)
    CHECKS.append(message)
def valid_type(v,t):
    if t in ('string','date','datetime'):return isinstance(v,str)
    if t=='boolean':return isinstance(v,bool)
    if t=='integer':return isinstance(v,int) and not isinstance(v,bool)
    if t=='number':return isinstance(v,(int,float)) and not isinstance(v,bool) and math.isfinite(v)
    if t=='object':return isinstance(v,dict)
    if t.startswith('array['):return isinstance(v,list) and all(valid_type(x,t[6:-1]) for x in v)
    raise ValueError(t)
def validate_row(row,spec,name):
    check(set(row)=={f['name'] for f in spec},f'{name}: exact fields')
    for f in spec:
        k=f['name'];v=row[k];typ=f['data_type']
        if v is None:check(f['nullable'],f'{name}.{k}: nullable');continue
        check(valid_type(v,typ),f'{name}.{k}: type {typ}')
        if f['allowed_values'] is not None:check(v in f['allowed_values'],f'{name}.{k}: enum')
        if typ=='date':
            check(bool(re.fullmatch(r'\d{4}-\d{2}-\d{2}',v)),f'{name}.{k}: ISO date format');dt.date.fromisoformat(v)
        if typ=='datetime':
            d=dt.datetime.fromisoformat(v);check(d.utcoffset() is not None,f'{name}.{k}: timezone')
def load():
    d=json.loads((OUT/'data_dictionary.json').read_text(encoding='utf-8'));tables={}
    for fn,cols in SCHEMAS.items():
        data=(OUT/fn).read_bytes();data.decode('utf-8');check(not data.startswith(b'\xef\xbb\xbf'),fn+': UTF-8 no BOM')
        spec=d['files'][fn]['fields'];check([x['name'] for x in spec]==cols,fn+': dictionary/header contract')
        if fn.endswith('.csv'):
            with (OUT/fn).open(encoding='utf-8',newline='') as f:
                reader=csv.DictReader(f);check(reader.fieldnames==cols,fn+': exact CSV header');raw=list(reader)
            rows=[]
            for r in raw:
                check(None not in r,fn+': correct CSV quoting')
                out={}
                for s in spec:
                    k=s['name'];v=r[k];t=s['data_type']
                    if v=='':out[k]=None
                    elif t in ['object','boolean'] or t.startswith('array['):out[k]=json.loads(v)
                    elif t=='integer':out[k]=int(v)
                    elif t=='number':out[k]=float(v)
                    else:out[k]=v
                rows.append(out)
        else:
            lines=data.decode().splitlines();check(all(x.strip() for x in lines),fn+': no blank JSONL records');rows=[json.loads(x) for x in lines]
        for i,r in enumerate(rows):validate_row(r,spec,f'{fn}[{i}]')
        tables[fn]=rows
    for fn in ['README.md','CODEX_CONTEXT.md','quality_report.md']:
        content=(OUT/fn).read_text(encoding='utf-8');check(len(content)>100,fn+': nonempty UTF-8 Markdown')
    check(set(p.name for p in OUT.iterdir() if p.is_file())==set(d['files']), 'dictionary covers every delivered file')
    return tables,d
def main():
    tables,d=load();sources={(r['source_id'],r['source_version']):r for r in tables['sources.csv']}
    check(len(sources)==len(tables['sources.csv']),'source composite keys unique')
    check(len(sources)==18,'18 current listed reports')
    check(sum(s['page_count'] for s in sources.values())==812,'812 PDF pages')
    check(len({s['file_sha256'] for s in sources.values()})==18,'no identical PDF hashes among listed reports')
    for s in sources.values():
        check(s['source_version']==s['file_sha256'][:16],'source version matches SHA256')
        check(bool(re.fullmatch('[0-9a-f]{64}',s['file_sha256'])),'valid SHA256')
        check(s['actual_publication_at'] is None and not s['original_version_verified'],'no fabricated historical publication or original vintage')
        check(s['available_at']==s['public_access_verified_at']==s['collected_at'],'conservative availability bound')
        check(all(1<=p<=s['page_count'] for p in s['analyzed_pages']+s['ocr_pages']),'source page bounds')
        check(dt.datetime.fromisoformat(s['first_discovered_at'])<=dt.datetime.fromisoformat(s['collected_at']),'discovery before collection')
    all_ids=set();normal_ids=set();derived=[]
    for fn,rows in tables.items():
        ids=[r.get('record_id',r.get('sample_id')) for r in rows] if fn!='sources.csv' else []
        check(len(ids)==len(set(ids)),fn+': record keys unique')
        if fn not in ['excluded_records.jsonl','sources.csv']:normal_ids.update(ids)
        for r in rows:
            if fn=='excluded_records.jsonl':
                payload=r['original_record'];check(r['dataset_file'] in SCHEMAS,'quarantine payload known schema')
                validate_row(payload,d['files'][r['dataset_file']]['fields'],r['record_id']+'.payload')
                check(payload['record_id']==r['original_record_id'],'quarantine retains original ID')
                check(payload['quality_status']=='quarantined','quarantine marked')
                check(not r['training_eligible'],'quarantine training disabled')
                continue
            if fn=='sources.csv':continue
            if 'source_id' in r:
                key=r['source_id'],r['source_version'];check(key in sources,fn+': source FK valid')
                s=sources[key];check(all(isinstance(p,int) and 1<=p<=s['page_count'] for p in r['source_pages']),fn+': physical PDF page valid')
                check(r['available_at']==s['available_at'],fn+': version availability matches source')
                check(not r['training_eligible'] and not r['historical_backtest_eligible'],fn+': no unapproved learning/backtest')
                check(r['quality_status']!='quarantined',fn+': quarantine absent from regular data')
            if r.get('period_start') and r.get('period_end'):check(r['period_start']<=r['period_end'],fn+': ordered observation interval')
            if r.get('ticker') and r.get('country')=='KR':check(bool(re.fullmatch(r'\d{6}',r['ticker'])),fn+': KR leading-zero code retained')
            if 'calculation_inputs_json' in r:
                inp=r['calculation_inputs_json']
                if inp and 'numeric_input' in inp:
                    expected=float(Decimal(str(inp['numeric_input']))*Decimal(str(inp['scale'])))
                    check(math.isclose(expected,r['normalized_value'],abs_tol=1e-10,rel_tol=1e-12),fn+': normalization recomputed')
                if inp and 'record_ids' in inp:derived.append(r)
            if fn=='portfolio_holdings.csv':
                w=r['weight_ratio'];check(w is None or 0<=w<=1,'holdings weights in [0,1]')
                check(not (w==0 and r['market_value']>0),'holdings zero/nonzero conflict excluded')
                if r['return_ratio'] is not None and r['price_ratio_return_check'] is not None:
                    check(abs(r['return_ratio']-r['price_ratio_return_check'])<=0.0025,'holdings return conflict excluded')
                check(r['operation_mode']=='unconfirmed' and r['price_type']=='reported_valuation_not_execution','no fabricated trades')
            if fn=='portfolio_changes.csv':
                check(r['retrospective'] and r['execution_at'] is None and not r['exact_execution_time_verified'],'changes kept retrospective without fabricated execution')
                if r['period_precision']=='part_of_month':check(r['event_date'] is None,'no arbitrary exact dates for fuzzy periods')
    for r in tables['excluded_records.jsonl']:
        check(r['original_record_id'] not in normal_ids,'quarantine disjoint from ordinary data')
        p=r['original_record'];check((p['source_id'],p['source_version']) in sources,'quarantine source FK')
    lookup={r['record_id']:r for fn,rows in tables.items() if fn not in ['sources.csv','excluded_records.jsonl'] for r in rows}
    for r in derived:
        ids=r['calculation_inputs_json']['record_ids'];check(all(x in lookup for x in ids),'derived input FK')
        a,b=[lookup[x]['normalized_value'] for x in ids];check(math.isclose((a-b)*100,r['normalized_value'],abs_tol=1e-12),'derived percentage-point spread recomputed')
    for fn,key in [('industry_metrics.csv',lambda r:(r['source_id'],r['source_version'],r['entity_id'],r['metric_name'],r['observation_period'],r['value_kind'])),
                   ('macro_metrics.csv',lambda r:(r['source_id'],r['source_version'],r['country'],r['metric_name'],r['observation_period'],r['value_kind'])),
                   ('portfolio_holdings.csv',lambda r:(r['snapshot_id'],r['entity_id']))]:
        check(len(tables[fn])==len({key(r) for r in tables[fn]}),fn+': observation keys unique')
    check((OUT/'training_dataset.jsonl').stat().st_size==0,'training file truly empty (0 bytes)')
    check(all(x['training_eligible'] is False for x in tables['sources.csv']),'all reports excluded from training')
    # Full overview rows are audit inputs, not an approved portfolio reconstruction.
    import curated_records as c
    values=[Decimal(x.split('|')[3]) for x in c.HOLDINGS['glif_am_06']['rows'].strip().splitlines()]
    check(sum(values)==Decimal('559574'),'documented account total mismatch measured')
    registry=json.loads((ROOT/'inputs/entity_verification.json').read_text())['entities']
    for fn,rows in tables.items():
        for r in rows:
            if r.get('identity_status')=='current_directory_verified_historical_unverified':
                e=registry[r['entity_id']];check(all(r[k]==e[k] for k in ['ticker','exchange','country','identity_source_url']),fn+': verified current security identity')
    result={'status':'passed','checks':len(CHECKS),'record_counts':{fn:len(v) for fn,v in tables.items()},
            'duplicate_keys':0,'schema_errors':0,'foreign_key_errors':0,'invalid_dates':0,'unit_conversion_errors':0,
            'external_numeric_truth_validated':False,'historical_backtest_eligible_records':0,'training_samples':0}
    audit=ROOT/'validation';audit.mkdir(exist_ok=True)
    (audit/'validation_results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    p=OUT/'quality_report.md';text=p.read_text()
    status=f"기계 검증: **통과**. {len(CHECKS):,}개 assertion 검사, 키 중복 0, 스키마/외부키/날짜형식/단위 변환 오류 0. 원문 사실성·과거 공개시각 미확인은 해소되지 않았다. 재현 결과: 저장소 `validation/validation_results.json`."
    text=re.sub(r'(<!-- VALIDATION_STATUS -->).*?(<!-- /VALIDATION_STATUS -->)',lambda m:m[1]+'\n'+status+'\n'+m[2],text,flags=re.S)
    p.write_text(text,encoding='utf-8')
    hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(OUT.iterdir()) if p.is_file()}
    (audit/'validated_file_hashes.json').write_text(json.dumps(hashes,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
