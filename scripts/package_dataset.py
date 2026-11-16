#!/usr/bin/env python3
"""Package only the documented UTF-8 delivery, never PDFs or credentials."""
import hashlib,json,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'glif_investment_dataset'
def main():
    validation=json.loads((ROOT/'validation/validation_results.json').read_text())
    assert validation['status']=='passed'
    hashes=json.loads((ROOT/'validation/validated_file_hashes.json').read_text())
    assert all(hashlib.sha256((DATA/name).read_bytes()).hexdigest()==digest for name,digest in hashes.items()),'Rerun validation after edits'
    dictionary=json.loads((DATA/'data_dictionary.json').read_text())
    names=sorted(dictionary['files'])
    assert sorted(p.name for p in DATA.iterdir())==names
    dest=ROOT/'glif_investment_dataset_2026-11-17.zip'
    with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name in names:z.write(DATA/name,arcname='glif_investment_dataset/'+name)
    with zipfile.ZipFile(dest) as z:
        assert z.testzip() is None
        assert len(z.infolist())==len(names)
        for name in names:assert z.read('glif_investment_dataset/'+name)==(DATA/name).read_bytes()
    manifest={'zip':dest.name,'zip_sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'zip_bytes':dest.stat().st_size,
        'files':[{ 'name':name,'bytes':(DATA/name).stat().st_size,'sha256':hashlib.sha256((DATA/name).read_bytes()).hexdigest()} for name in names]}
    (ROOT/'validation/artifact_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(manifest,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
