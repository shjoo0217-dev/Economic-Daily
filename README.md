# Economic-Daily — GLIF 공개 투자 연구 데이터

2026-11-17 (Asia/Seoul)에 GLIF 공개 보고서 18개를 수집하고 선택 본문을 분석한 데이터셋이다. 작업은 이 저장소의 연결된 Codex Cloud 체크아웃에서 수행했다.

먼저 [CODEX_CONTEXT.md](glif_investment_dataset/CODEX_CONTEXT.md), [데이터 README](glif_investment_dataset/README.md), [품질 보고서](glif_investment_dataset/quality_report.md)를 읽는다.

## 데이터와 오류 처리

기본 파일 12개에 사용자 요청을 반영한 `excluded_records.jsonl`을 추가했다. 이 파일의 18개 상충/의심 레코드는 감사 전용이며 기본 데이터에서 격리했다. `training_dataset.jsonl`은 실제 0바이트 파일이다. 모든 자료는 `training_eligible=false`, `historical_backtest_eligible=false`이며, 공개시점·원버전·원자료 사실성과 미래 시장 라벨 확보 전에는 학습/과거 백테스트에 사용할 수 없다.

## 재생성

```bash
python scripts/build_dataset.py
python scripts/validate_dataset.py
python scripts/package_dataset.py
```

위 3개 명령은 Python 3.10+ 표준 라이브러리만으로 동작하며 외부 네트워크 없이 이번 검토본을 재생성한다. `inputs/`는 수집 메타데이터, 공개 종목 식별 증거, API 문서 접근 결과다. `scripts/curated_records.py`는 원문 페이지와 연결된 선별 전사·요약이다.

추가 수집에는 `collect_glif.py`(PyMuPDF), 이미지 보고서 OCR에는 `ocr_glif.py`(PyMuPDF, Tesseract eng), 검토 후 메타데이터 동결에는 `prepare_snapshot.py`(pandas, HTML parser)를 사용한다. 새 PDF 해시를 검토 없이 기존 추출값에 연결하면 안 된다. `audit_source_evidence.py`는 로컬 비공개 캐시가 있을 때 PDF 해시와 숫자 문자열을 검증한다.

`validation/validation_results.json`은 스키마·키·페이지·단위·날짜·격리 검증 결과이고, `validation/evidence_results.json`은 원문 숫자 문자열 및 PDF 해시 대조 결과다. `validation/artifact_manifest.json`은 배포 ZIP과 각 파일의 SHA-256이다. 코드나 입력을 변경하면 재생성·검증·압축을 순서대로 실행한다.

## 수집 및 제외 원칙

공개 목록에 직접 연결된 PDF만 수집했다. 원본 PDF와 전체 추출 텍스트·OCR 이미지·전체 종목 디렉터리는 `.cache/`에 저장하며 Git과 배포 ZIP에 포함하지 않는다. 내부 원장·DCF·실체결 로그는 확보하지 않았다. 공개 PDF에 인용된 유료 원자료의 재배포·학습 권한을 가정하지 않는다.

실시간 시세·호가·체결·주문 API와 DART 공시, ALFRED 빈티지, 기업행사·거래비용 데이터는 별도 연결해야 한다. 이번 결과는 주·월 단위 투자 연구를 위한 검증 대기 참고자료이며, 자동 주문 또는 수익성 검증이 완료된 시스템이 아니다.
