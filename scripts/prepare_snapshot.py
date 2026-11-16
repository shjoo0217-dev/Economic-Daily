"""Freeze collected metadata and public security-directory evidence for offline rebuilds."""
import csv, datetime as dt, hashlib, io, json, re
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
CACHE=Path((ROOT/'.cache/LATEST').read_text())
OUT=ROOT/'inputs';OUT.mkdir(exist_ok=True)
m=json.loads((CACHE/'manifest.json').read_text())
for r in m['reports']:
    pages=json.loads((CACHE/f"{r['source_id']}.pages.json").read_text()) if r['access_status']=='downloaded' else []
    refs={}
    for n,t in enumerate(pages,1):
        if r['source_id']=='glif_am_04':
            t=(CACHE/'ocr'/f'glif_am_04_p{n:03}.txt').read_text()
        for line in t.splitlines():
            for match in re.finditer(r'(?:자료|출처|Source)\s*[:：]\s*(.+?)(?=(?:자료|출처|Source)\s*[:：]|$)',line,re.I):
                ref=re.sub(r'\s+',' ',match.group(1)).strip()
                if ref:refs.setdefault(ref,[]).append(n)
    r['upstream_sources']=[{'citation_raw':k,'source_pages':sorted(set(v)),
        'verification_status':'page_caption_only_not_primary_verified','terms_status':'unverified'} for k,v in refs.items()]
    r.pop('local_pdf_path',None)
    r['pdf_metadata']={k:v for k,v in r['pdf_metadata'].items() if k in ('creationDate','modDate','producer','format')}
(OUT/'source_snapshot.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')

registry={};access=[]
for name,exchange,endpoint in [('krx_kospi.html','KOSPI','stockMkt'),('krx_kosdaq.html','KOSDAQ','kosdaqMkt')]:
    p=ROOT/'.cache/external'/name
    data=p.read_bytes();url=f'https://kind.krx.co.kr/corpgeneral/corpList.do?method=download&marketType={endpoint}'
    at=dt.datetime.fromtimestamp(p.stat().st_mtime,dt.timezone.utc).isoformat(timespec='seconds')
    df=pd.read_html(io.StringIO(data.decode('euc-kr')),converters={'종목코드':str})[0]
    access.append({'url':url,'sha256':hashlib.sha256(data).hexdigest(),'collected_at':at,'row_count':len(df),'purpose':'current_security_identity_only'})
    for _,r in df.iterrows():
        ticker=str(r['종목코드']).zfill(6)
        registry['KR:'+ticker]={'entity_id':'KR:'+ticker,'entity_name':r['회사명'],'ticker':ticker,'exchange':exchange,
            'country':'KR','identity_source_url':url,'identity_verified_at':at,'identity_status':'current_directory_verified_historical_unverified'}
for name,key,exchange in [('nasdaqlisted.txt','Symbol','NASDAQ'),('otherlisted.txt','ACT Symbol',None)]:
    p=ROOT/'.cache/external'/name;data=p.read_bytes();url='https://www.nasdaqtrader.com/dynamic/SymDir/'+name
    at=dt.datetime.fromtimestamp(p.stat().st_mtime,dt.timezone.utc).isoformat(timespec='seconds')
    rows=list(csv.DictReader(data.decode().splitlines(),delimiter='|'))
    access.append({'url':url,'sha256':hashlib.sha256(data).hexdigest(),'collected_at':at,
        'provider_file_creation_raw':data.decode().splitlines()[-1],'purpose':'current_security_identity_only'})
    for r in rows:
        ticker=r[key]
        if not ticker or 'File Creation' in ticker or r.get('Test Issue')=='Y':continue
        registry['US:'+ticker]={'entity_id':'US:'+ticker,'entity_name':r['Security Name'],'ticker':ticker,
            'exchange':exchange or {'N':'NYSE','P':'NYSE_ARCA','Z':'CBOE_BZX','A':'NYSE_AMERICAN','V':'IEX'}.get(r.get('Exchange')),
            'country':'US','identity_source_url':url,'identity_verified_at':at,'identity_status':'current_directory_verified_historical_unverified'}
# Only selected public identity rows are retained in the reproducibility inputs.
kr=['000660','005930','042700','095340','078930','010950','096770','011930','066570','010140','042660','439260','267260','103590','207940','128940','189300','012450','103140','079550','278470','192820','083650','034020']
us=['APP','COST','CSCO','EWJV','GOOG','IBB','IEF','IEI','MRVL','MU','NVDA','PANW','PLTR','RKLB','SHY','SMH','SNDK','TLT','TSLA','VRTX','XOVR','CPER','CRS','FXY','HII','IAU','IBM','IGV','JNJ','KMI','LLY','PM','RBLX','RDDT','SHV','SHYG','USO','VRT','WM','XLE','VIXY','CLS']
keys=['KR:'+t for t in kr]+['US:'+t for t in us]
selected={k:registry[k] for k in keys if k in registry}
(OUT/'entity_verification.json').write_text(json.dumps({'access':access,'entities':selected},ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'documentation_access.json').write_bytes((ROOT/'.cache/external/documentation_access.json').read_bytes())
print('Frozen',len(m['reports']),'reports;',len(selected),'public security identities; missing:',[k for k in keys if k not in registry])
