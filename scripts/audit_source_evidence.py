#!/usr/bin/env python3
"""Optional private-cache audit: source hashes and exact literal numeric evidence."""
import hashlib,json,re,unicodedata
from pathlib import Path
import curated_records as C
ROOT=Path(__file__).resolve().parents[1]
def norm(x):return re.sub(r'\s+','',unicodedata.normalize('NFKC',x))
def main():
    cache=Path((ROOT/'.cache/LATEST').read_text())
    snapshot=json.loads((ROOT/'inputs/source_snapshot.json').read_text())
    for r in snapshot['reports']:
        assert hashlib.sha256((cache/(r['source_id']+'.pdf')).read_bytes()).hexdigest()==r['file_sha256']
    results=[]
    for row in C.INDUSTRY+C.MACRO:
        pages=json.loads((cache/(row['source_id']+'.pages.json')).read_text())
        present=norm(row['original_value']) in norm(' '.join(pages[n-1] for n in row['source_pages']))
        results.append({'source_id':row['source_id'],'source_pages':row['source_pages'],
            'metric_name':row['metric_name'],'original_value':row['original_value'],'literal_found':present})
    assert all(x['literal_found'] for x in results)
    audit={'pdf_hashes_verified':len(snapshot['reports']),'numeric_literals_verified':len(results),
           'external_factual_accuracy_verified':False,'results':results,
           'visual_review_pages':{'glif_am_02':[32],'glif_am_04':[36],'glif_am_05':[26],'glif_am_06':[44],
               'glif_im_07':[1],'glif_im_08':[38],'glif_im_09':[33]}}
    (ROOT/'validation/evidence_results.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Verified 18 PDF hashes and',len(results),'literal observations; external numeric truth NOT validated.')
if __name__=='__main__':main()
