#!/usr/bin/env python3
"""Download only PDFs explicitly listed at the public GLIF projects page.

Full PDFs/text stay in .cache and are not included in redistribution artifacts.
Uses Python stdlib and PyMuPDF. Rerunning creates a new timestamped capture.
"""
import concurrent.futures
import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
INDEX = 'https://glifskku.com/projects.html'

def now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')

def fetch(url):
    url = urllib.parse.quote(url, safe=':/?=&%')
    req = urllib.request.Request(url, headers={'User-Agent':'GLIF-public-research-dataset/1.0'})
    with urllib.request.urlopen(req, timeout=45) as response:
        return response.read(), dict(response.headers), response.geturl(), response.status

def main():
    import fitz
    capture = ROOT / '.cache' / now().replace(':','').replace('+','_')
    capture.mkdir(parents=True)
    discovered = now()
    html, headers, final_url, status = fetch(INDEX)
    (capture/'projects.html').write_bytes(html)
    body = html.decode('utf-8')
    pattern = r"\{\s*id:\s*(\d+),\s*name:\s*'([^']+)',\s*term:\s*'([^']+)',\s*date:\s*'([^']+)',\s*url:\s*'([^']+)'\s*\}"
    reports = []
    for ident,title,term,date,url in re.findall(pattern,body):
        team = 'im' if '/im_' in url else 'am'
        reports.append(dict(source_id=f'glif_{team}_{int(ident):02d}', title=title,
            team='IM팀' if team=='im' else '자산운용팀', semester=term,
            report_type='industry' if team=='im' else ('gaa' if 'Allocation' in title else 'market_view'),
            listed_publication_date=date, source_url=urllib.parse.urljoin(INDEX,url),
            listing_url=INDEX, first_discovered_at=discovered, listed=True))
    if not reports:
        raise RuntimeError('No reports parsed; review current site schema.')
    def download(r):
        r['access_attempted_at']=now()
        try:
            data,h,final,s = fetch(r['source_url'])
            r.update(http_status=s, final_url=final, http_last_modified=h.get('Last-Modified'), http_etag=h.get('ETag'))
            if not data.startswith(b'%PDF-'):
                raise ValueError('HTTP response is not a PDF')
            path=capture/(r['source_id']+'.pdf')
            path.write_bytes(data)
            doc=fitz.open(path)
            pages=[p.get_text(sort=True) for p in doc]
            r.update(access_status='downloaded', downloaded_at=now(), file_sha256=hashlib.sha256(data).hexdigest(),
                file_size_bytes=len(data), page_count=len(doc), pdf_metadata=doc.metadata,
                local_pdf_path=str(path), nonempty_text_pages=sum(bool(x.strip()) for x in pages),
                failure_reason=None)
            (capture/(r['source_id']+'.pages.json')).write_text(json.dumps(pages,ensure_ascii=False,indent=2),encoding='utf-8')
            (capture/(r['source_id']+'.txt')).write_text('\n\n'.join(f'=== PDF PAGE {i} ===\n{p}' for i,p in enumerate(pages,1)),encoding='utf-8')
        except Exception as e:
            r.update(access_status='failed',failure_reason=f'{type(e).__name__}: {e}')
            if hasattr(e,'code'): r['http_status']=e.code
        return r
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        reports=list(pool.map(download,reports))
    manifest=dict(captured_at=discovered,listing_url=INDEX,listing_sha256=hashlib.sha256(html).hexdigest(),
        listing_response_headers=headers,listing_status=status,listing_final_url=final_url,reports=reports)
    (capture/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    (ROOT/'.cache'/'LATEST').write_text(str(capture),encoding='utf-8')
    print(json.dumps({'capture':str(capture),'reports':[{k:r.get(k) for k in ('source_id','title','access_status','page_count','nonempty_text_pages','failure_reason')} for r in reports]},ensure_ascii=False,indent=2))

if __name__=='__main__': main()
