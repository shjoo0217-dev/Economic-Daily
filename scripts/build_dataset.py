#!/usr/bin/env python3
"""Rebuild the delivery offline from frozen metadata and reviewed curation."""
import calendar, collections, csv, datetime as dt, hashlib, json, re
from decimal import Decimal
from pathlib import Path
import curated_records as C
from schema import SCHEMAS,dictionary

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'glif_investment_dataset'
VERSION='2026-11-17.v1'
SNAP=json.loads((ROOT/'inputs/source_snapshot.json').read_text())
REG=json.loads((ROOT/'inputs/entity_verification.json').read_text())
REPORTS={r['source_id']:r for r in SNAP['reports']}
TABLES={f:[] for f in SCHEMAS}
COUNTERS=collections.Counter()
PORTFOLIOS={'glif_am_02':'GLIF_GAA_25_1','glif_am_04':'GLIF_GAA_25_2','glif_am_06':'GLIF_GAA_26_1'}

def number(v):
    return None if v is None or v=='' else float(Decimal(str(v)))
def div100(v):return None if v is None or v=='' else float(Decimal(str(v))/100)
def json_text(v):return json.dumps(v,ensure_ascii=False,separators=(',',':'),allow_nan=False)
def new_id(prefix):COUNTERS[prefix]+=1;return f'{prefix}_{COUNTERS[prefix]:04}'
def clean_row(fn,row):
    extra=set(row)-set(SCHEMAS[fn])
    if extra:raise ValueError((fn,'unknown fields',extra))
    return {k:row.get(k) for k in SCHEMAS[fn]}
def emit(fn,row):TABLES[fn].append(clean_row(fn,row))
def quarantine(fn,row,reasons):
    row=dict(row,quality_status='quarantined',review_required=True,training_eligible=False,historical_backtest_eligible=False)
    row['quality_flags']=sorted(set(row.get('quality_flags',[])+reasons))
    emit('excluded_records.jsonl',dict(record_id=new_id('excluded'),original_record_id=row['record_id'],
        source_id=row['source_id'],source_pages=row['source_pages'],dataset_file=fn,reason_codes=reasons,
        original_record=clean_row(fn,row),release_conditions='원보고서 및 해당 수치의 1차 출처·단위·기준기간·버전을 대조하고 독립 검토 후 새 버전으로 승인. 현재 학습·신호 생성·성과 검증에 사용 금지.',training_eligible=False))
def common(sid,pages,kind='pdf_text',flags=None):
    r=REPORTS[sid]
    return dict(source_id=sid,source_pages=pages,source_version=r['file_sha256'][:16],
        available_at=r['downloaded_at'],collected_at=r['downloaded_at'],evidence_kind=kind,
        quality_status='needs_primary_verification',quality_flags=sorted(set((flags or [])+['upstream_numeric_truth_not_verified','historical_publication_and_version_unverified'])),
        review_required=True,training_eligible=False,historical_backtest_eligible=False)
def identity(key,reported=None):
    if key in REG['entities']:
        return {**REG['entities'][key],'reported_ticker':reported}
    return dict(entity_id=key,entity_name=key.split(':',1)[-1],reported_ticker=reported,ticker=None,exchange=None,country=None,
        identity_source_url=None,identity_verified_at=None,identity_status='not_applicable' if key.startswith(('INDUSTRY:','CASH:')) else 'unverified')
def key_for_ticker(t):
    t=t.rstrip('*')
    return 'KR:'+t[:-3] if t.endswith('.KS') else 'US:'+t
def period(p):
    if not p:return None,None,'unknown'
    if re.fullmatch(r'\d{4}-\d{2}-\d{2}',p):return p,p,'day'
    if re.fullmatch(r'\d{4}-\d{2}',p):
        y,m=map(int,p.split('-'));return f'{y}-{m:02}-01',f'{y}-{m:02}-{calendar.monthrange(y,m)[1]}','month'
    if re.fullmatch(r'\d{4}',p):return p+'-01-01',p+'-12-31','year'
    m=re.fullmatch(r'(\d{4})-([QH])(\d)',p)
    if m:
        y=int(m[1]); span=3 if m[2]=='Q' else 6;start=(int(m[3])-1)*span+1;end=start+span-1
        return f'{y}-{start:02}-01',f'{y}-{end:02}-{calendar.monthrange(y,end)[1]}','quarter' if span==3 else 'half_year'
    if re.fullmatch(r'\d{4}-\d{2}/\d{4}-\d{2}',p):
        a,b=p.split('/');return period(a)[0],period(b)[1],'month_range'
    return None,None,'fiscal_unresolved'

UNITS={'%':('ratio','0.01',None),'%p':('percentage_point','1',None),'억원':('KRW','100000000','KRW'),
 '조원':('KRW','1000000000000','KRW'),'억USD':('USD','100000000','USD'),'trillion_USD':('USD','1000000000000','USD'),
 '만명':('person','10000',None),'thousand_person':('person','1000',None),'barrel/day':('barrel/day','1',None),
 'multiple':('multiple','1',None),'vessel':('vessel','1',None),'litre':('litre','1',None),'vehicle':('vehicle','1',None),
 'USD':('USD','1','USD')}
def value_fields(r):
    unit,scale,currency=UNITS[r['original_unit']]
    a,b,precision=period(r['observation_period'])
    return {k:r[k] for k in ['metric_name','observation_period','original_value','original_unit','value_kind','value_qualifier','upstream_source_raw']} | dict(
        observation_period=None if precision=='fiscal_unresolved' else r['observation_period'],observation_period_raw=r['observation_period'],
        period_start=a,period_end=b,period_precision=precision,normalized_value=float(Decimal(str(r['numeric_input']))*Decimal(scale)),
        normalized_unit=unit,currency=currency,normalization_formula=f'numeric_input * {scale}',
        calculation_inputs_json={'numeric_input':r['numeric_input'],'original_unit':r['original_unit'],'scale':float(scale)})
def build_metrics():
    for r in C.INDUSTRY:
        reported=None
        if r['entity_id']=='KR:042660':reported='242660'
        elif r['entity_id'].startswith(('KR:','US:')):
            # Do not invent a printed ticker where the text layer omitted the label.
            if r['source_id'] not in ('glif_im_01','glif_im_03'):reported=r['entity_id'].split(':')[1]
        row=common(r['source_id'],r['source_pages'],flags=r['quality_flags']) | identity(r['entity_id'],reported) | value_fields(r) | dict(
            record_id=new_id('ind'),industry=r['industry'],financial_statement_scope=r['financial_statement_scope'])
        issues=[x for x in r['quality_flags'] if x in ['segment_shares_sum_91_percent_not_100','narrative_chart_period_mismatch']]
        if issues:quarantine('industry_metrics.csv',row,issues)
        else:emit('industry_metrics.csv',row)
    for r in C.MACRO:
        name=r['metric_name'];basis='YoY' if '_yoy' in name else 'MoM' if '_mom' in name else 'QoQ annualized (SAAR)' if '_saar' in name else 'see metric definition; unspecified aggregation'
        row=common(r['source_id'],r['source_pages'],flags=r['quality_flags']) | value_fields(r) | dict(
            record_id=new_id('mac'),country=r['country'],measurement_basis=basis,
            release_date_reported=r['release_date_reported'],release_at=None,revision_status=r['revision_status'],vintage_date=None)
        issues=[x for x in r['quality_flags'] if x.startswith('quarantine_') or x=='source_uses_percent_for_yield_difference']
        if issues:quarantine('macro_metrics.csv',row,issues)
        else:emit('macro_metrics.csv',row)
    # A calculation is a new, explicit observation; never silently fixes the original.
    inputs=[next(x for x in TABLES['macro_metrics.csv'] if x['source_id']=='glif_am_03' and x['metric_name']==m) for m in ('mortgage_rate_30y','treasury_yield_10y')]
    row=common('glif_am_03',[11],kind='derived',flags=['derived_yield_difference_not_original_quote']) | value_fields(dict(
        metric_name='mortgage_treasury_spread_derived',observation_period='2025-10-02',original_value=None,original_unit='%p',numeric_input=2.24,
        value_kind='derived',value_qualifier='exact',upstream_source_raw='FRED as cited by GLIF')) | dict(record_id=new_id('mac'),country='US',measurement_basis='difference of two quoted yields',release_date_reported=None,release_at=None,revision_status=None,vintage_date=None)
    row['original_unit']=None
    row['normalization_formula']='(input_mortgage_rate_ratio - input_treasury_yield_ratio) * 100'
    row['calculation_inputs_json']={'record_ids':[x['record_id'] for x in inputs]}
    row['normalized_value']=float((Decimal(str(inputs[0]['normalized_value']))-Decimal(str(inputs[1]['normalized_value'])))*100)
    emit('macro_metrics.csv',row)

def asset(t):
    if t=='CASH':return 'cash'
    if t in ['SHV','SHY','IEI','IEF','TLT','SHYG']:return 'bond_etf'
    if t in ['IAU','CPER','USO']:return 'commodity_etf'
    if t=='FXY':return 'currency_etf'
    if t in ['SMH','IGV','XOVR','EWJV','XLE','IBB']:return 'equity_etf'
    return 'equity'

def build_holdings():
    for sid,s in C.HOLDINGS.items():
        for line in s['rows'].strip().splitlines():
            ticker,avg,price,mv,ret,weight=line.split('|');base=ticker.rstrip('*');cash=base=='CASH'
            flags=[]
            if s['as_of'] is None:flags.append('snapshot_date_unconfirmed')
            if sid=='glif_am_06':flags.append('overview_sum_17_USD_above_account_value')
            if base.endswith('.KS'):flags.append('KR_security_reported_in_USD_no_FX_basis')
            price_check=None if not avg or not price else float(Decimal(price)/Decimal(avg)-1)
            row=common(sid,[s['page']],kind='table_visual_verified',flags=flags) | identity('CASH:USD' if cash else key_for_ticker(ticker),ticker) | dict(
                record_id=new_id('hold'),portfolio_id=PORTFOLIOS[sid],snapshot_id=sid+'_overview',as_of_date=s['as_of'],period_raw=s['period_raw'],
                asset_type=asset(base),holding_status='cash' if cash else ('exited_reported' if ticker.endswith('*') else 'held_reported' if weight and float(weight)>0 else 'unconfirmed'),
                currency='USD',average_price_raw='$'+avg if avg else None,average_price=number(avg),valuation_price_raw='$'+price if price else None,
                valuation_price=number(price),market_value_raw='$'+mv if mv else None,market_value=number(mv),weight_raw=weight+'%' if weight else None,
                weight_ratio=div100(weight),return_raw=ret+'%' if ret else None,return_ratio=div100(ret),
                return_realization=('realized' if ticker.endswith('*') else 'unrealized') if sid=='glif_am_06' and not cash else 'unconfirmed',
                price_type='reported_valuation_not_execution',operation_mode='unconfirmed',price_ratio_return_check=price_check,
                normalization_formula='weight_ratio=raw_weight_percent/100; return_ratio=raw_return_percent/100; price_ratio_return_check=valuation_price/average_price-1 (diagnostic only)',
                calculation_inputs_json={'average_price':number(avg),'valuation_price':number(price),'raw_return_percent':number(ret),'raw_weight_percent':number(weight)})
            reasons=[]
            if price_check is not None and ret and abs(price_check-float(ret)/100)>0.0025:
                reasons.append('reported_return_differs_from_simple_price_ratio_over_0_25pp_unresolved')
            if mv and weight and float(mv)>0 and float(weight)==0:
                reasons.append('positive_market_value_with_zero_weight_unresolved')
            if reasons:quarantine('portfolio_holdings.csv',row,reasons)
            else:emit('portfolio_holdings.csv',row)

def P(sid,page,metric,raw,n,unit,scope='portfolio',benchmark=None,cumulative=None,realization='unconfirmed',start=None,end=None,period_raw=None,flags=None):
    norm,scale,curr=UNITS[unit]
    row=common(sid,[page],kind='chart_printed_label_visual_verified' if metric=='cumulative_return' else 'pdf_text',flags=flags) | dict(
        record_id=new_id('perf'),portfolio_id=PORTFOLIOS[sid],performance_scope=scope,benchmark_name=benchmark,metric_name=metric,
        period_raw=period_raw,period_start=start,period_end=end,original_value=raw,original_unit=unit,normalized_value=float(Decimal(str(n))*Decimal(scale)),
        normalized_unit=norm,currency=curr,is_cumulative=cumulative,return_realization=realization,cost_inclusion='unconfirmed',operation_mode='unconfirmed',
        normalization_formula=f'numeric_input * {scale}',calculation_inputs_json={'numeric_input':n,'original_unit':unit,'scale':float(scale)})
    if metric=='net_realized_pnl':quarantine('portfolio_performance.csv',row,['reported_net_realized_pnl_minus1242_vs_components_minus1239'])
    else:emit('portfolio_performance.csv',row)
def build_performance():
    for sid,page,p,b,label,period_raw in [
      ('glif_am_02',32,6.31,-0.64,'Nasdaq Com Cumulative Return','그래프 축 4-Feb~4-Jun; 확정 시작·종료일 미상'),
      ('glif_am_04',36,8.31,3.24,'Nasdaq Com Cumulative Return','그래프 축 19-Sep~28-Nov; 확정 시작·종료일 미상'),
      ('glif_am_06',44,11.91,12.07,'S&P 500 Cumulative Return','Mar 6–Jun 3, 2026; p46 두 phase와 p44 각주')]:
        start='2026-03-06' if sid=='glif_am_06' else None;end='2026-06-03' if sid=='glif_am_06' else None
        flags=['benchmark_elsewhere_labeled_Nasdaq','year_from_report_context'] if sid=='glif_am_06' else ['performance_boundaries_unconfirmed']
        P(sid,page,'cumulative_return',f'{p}%',p,'%',cumulative=True,start=start,end=end,period_raw=period_raw,flags=flags)
        P(sid,page,'cumulative_return',f'{b}%',b,'%',scope='benchmark',benchmark=label,cumulative=True,start=start,end=end,period_raw=period_raw,flags=flags)
    P('glif_am_02',32,'total_commissions','$204.79',204.79,'USD',period_raw='p32 Total Commissions; 집계 기간 명시 없음')
    P('glif_am_06',46,'total_account_value','$559,557',559557,'USD',period_raw='p44/46 overview through Jun 3',flags=['holdings_sum_differs_by_17_USD'])
    P('glif_am_06',46,'unrealized_pnl','+$60,799',60799,'USD',realization='unrealized',period_raw='p46 account overview')
    P('glif_am_06',46,'net_realized_pnl','−$1,242',-1242,'USD',realization='realized',period_raw='p46 account overview')

def build_changes_and_notes():
    for r in C.CHANGES:
        row=common(r['source_id'],r['source_pages'],kind='ocr_text_reviewed' if r['source_id']=='glif_am_04' else 'pdf_text',flags=r['quality_flags']) | identity(key_for_ticker(r['reported_ticker']),r['reported_ticker']) | dict(
            record_id=new_id('change'),portfolio_id=PORTFOLIOS[r['source_id']],period_raw=r['period_raw'],period_precision='reported_day' if r['event_date'] else 'part_of_month',
            event_date=r['event_date'],execution_at=None,exact_execution_time_verified=False,retrospective=True,action=r['action'],weight_before_ratio=None,weight_after_ratio=None,
            weight_change_raw=None if r['weight_change_pp'] is None else str(r['weight_change_pp'])+'%p',weight_change_pp=r['weight_change_pp'],
            rationale=r['rationale'],market_event=r['market_event'],operation_mode='unconfirmed')
        emit('portfolio_changes.csv',row)
    for r in C.NOTES:
        row=common(r['source_id'],r['source_pages'],kind='ocr_text_reviewed' if r['source_id']=='glif_am_04' else 'pdf_text',flags=r['quality_flags']) | {
            k:(v if v!=[] else None) for k,v in r.items() if k not in ['source_id','source_pages','quality_flags']} | dict(
            record_id=new_id('note'),content_type='report_opinion_summary',fact_claims=None,analyst_labels=None)
        emit('research_notes.jsonl',row)

def pdfdate(raw):
    if not raw:return None
    m=re.match(r'D:(\d{14})(Z|[+-]\d{2}.*)?',raw)
    if not m:return None
    date=dt.datetime.strptime(m[1],'%Y%m%d%H%M%S'); tz=m[2]
    if tz is None:return None
    if tz.startswith('Z'):offset=dt.timezone.utc
    else:
        nums=re.findall(r'\d+',tz);minutes=int(nums[0])*60+(int(nums[1]) if len(nums)>1 else 0)
        offset=dt.timezone(dt.timedelta(minutes=minutes*(1 if tz[0]=='+' else -1)))
    return date.replace(tzinfo=offset).isoformat()
PRINTED={
 'glif_im_01':('2025-04-11','p1 2025년04월11일'),
 'glif_im_02':('2025-04-11','p1 2025.04; p33 2025.4.11'),
 'glif_im_03':('2025-08-14','p1 2025년08월14일'),
 'glif_im_04':('2025-10-10','p1 2025년10월10일'),
 'glif_im_05':('2025-10-10','p1 2025년10월10일'),
 'glif_im_06':('2026-01-28','p1 2026년1월28일; 목록은 2026-01-31'),
 'glif_im_07':('2025-02-06','p1 2025년02월06일 (이미지 대조); 본문 p35 2026.02.06; 목록 2026-01-31'),
 'glif_im_08':('2026-04-10','p1 2026년4월10일'),
 'glif_im_09':('2026-04-10','p1 2026년04월10일'),
 'glif_im_10':('2026-10-09','p1 2026년10월9일; 목록 2026-10-10'),
 'glif_im_11':('2026-10-09','p1 2026년10월09일; 목록 2026-10-10'),
 'glif_am_01':('2025-04-11','PDF p4, p11: 2025.4.11')}
def build_sources():
    for sid,r in REPORTS.items():
        pages=set([1])
        for fn,rows in TABLES.items():
            if fn=='sources.csv':continue
            for row in rows:
                if row.get('source_id')==sid:pages.update(row['source_pages'])
        # Metadata and conflict-only pages that were explicitly inspected.
        pages.update({'glif_am_02':[2,16,20,21,68],'glif_am_04':[2,35,37,60,61,62,64,65,66,73],
          'glif_am_06':[2,3,4,45,46,47,58,60,65,67,69,70,71,73,75,80,81,82],
          'glif_am_05':[2,16,26],'glif_am_07':[2,48],
          'glif_im_02':[1,32,33],'glif_im_03':[2,3,10,16,25,32]}.get(sid,[]))
        printed,evidence=PRINTED.get(sid,(None,'선택 검토에서 독립적인 PDF 발간일을 확인하지 못함; 목록 날짜로 대체하지 않음'))
        meta=r.get('pdf_metadata',{});created=pdfdate(meta.get('creationDate'));modified=pdfdate(meta.get('modDate'))
        flags=['historical_publication_unknown','first_public_version_unverified','upstream_licenses_unverified']
        if printed and printed!=r['listed_publication_date']:flags.append('listing_vs_printed_date_conflict')
        if any(x and x[:10]>r['listed_publication_date'] for x in [created,modified]):flags.append('pdf_metadata_later_than_listed_publication')
        if sid in ['glif_im_01','glif_im_02','glif_im_03','glif_im_04','glif_im_10']:flags.append('pdf_font_or_text_layout_anomalies')
        emit('sources.csv',dict(source_id=sid,source_version=r['file_sha256'][:16],title=r['title'],team=r['team'],report_type=r['report_type'],semester=r['semester'],
          listed_publication_date=r['listed_publication_date'],printed_publication_date=printed,printed_date_evidence=evidence,
          actual_publication_at=None,public_access_verified_at=r['downloaded_at'],first_discovered_at=r['first_discovered_at'],collected_at=r['downloaded_at'],
          available_at=r['downloaded_at'],availability_basis='current_download_conservative_bound',listing_url=r['listing_url'],source_url=r['source_url'],final_url=r.get('final_url'),
          listed=True,access_status=r['access_status'],http_status=r.get('http_status'),failure_reason=r.get('failure_reason'),page_count=r.get('page_count'),file_size_bytes=r.get('file_size_bytes'),
          file_sha256=r.get('file_sha256'),pdf_creation_at=created,pdf_modified_at=modified,pdf_dates_raw={k:meta.get(k) for k in ['creationDate','modDate']},
          original_version_verified=False,analysis_status='selected_pages_analyzed',analyzed_pages=sorted(pages),text_extracted_pages=r.get('nonempty_text_pages'),
          ocr_pages=list(range(1,74)) if sid=='glif_am_04' else [],upstream_sources=r['upstream_sources'],license_status='not_verified_no_raw_pdf_redistribution',
          quality_flags=flags,training_eligible=False,historical_backtest_eligible=False))

def write_files():
    OUT.mkdir(exist_ok=True)
    for fn,rows in TABLES.items():
        p=OUT/fn
        if fn.endswith('.csv'):
            with p.open('w',encoding='utf-8',newline='') as f:
                writer=csv.DictWriter(f,fieldnames=SCHEMAS[fn]);writer.writeheader()
                for row in rows:
                    writer.writerow({k:'' if v is None else json_text(v) if isinstance(v,(dict,list,bool)) else v for k,v in row.items()})
        else:
            p.write_text(''.join(json_text(row)+'\n' for row in rows),encoding='utf-8')
    (OUT/'data_dictionary.json').write_text(json.dumps(dictionary(VERSION),ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')

def main():
    build_metrics();build_holdings();build_performance();build_changes_and_notes();build_sources();write_files()
    from write_docs import write_docs
    write_docs(ROOT,OUT,TABLES,SNAP,REG,VERSION)
    print(json.dumps({fn:len(rows) for fn,rows in TABLES.items()},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
