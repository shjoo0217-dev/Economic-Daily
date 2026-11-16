#!/usr/bin/env python3
"""OCR selected pages into the private cache; numeric output requires review."""
import concurrent.futures, json, os, subprocess
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[1]
CACHE=Path((ROOT/'.cache/LATEST').read_text())
def ocr(task):
    sid,n=task
    folder=CACHE/'ocr';folder.mkdir(exist_ok=True)
    out=folder/f'{sid}_p{n:03}'
    if out.with_suffix('.txt').exists():return
    doc=fitz.open(CACHE/f'{sid}.pdf')
    doc[n-1].get_pixmap(dpi=160).save(str(out)+'.png')
    subprocess.run(['tesseract',str(out)+'.png',str(out),'-l','eng','--psm','3'],
        check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,env={**os.environ,'OMP_THREAD_LIMIT':'1'})
def main():
    tasks=[('glif_am_04',n) for n in range(1,74)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for _ in pool.map(ocr,tasks):pass
    print('OCR completed:',len(tasks),'pages; machine text is unverified.')
if __name__=='__main__':main()
