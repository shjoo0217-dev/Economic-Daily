# GLIF 투자 연구 데이터셋

버전: 2026-11-17.v1. 수집 기준: **2026-11-17T01:34:01+09:00 (Asia/Seoul)** / 2026-11-16T16:34:01+00:00 (UTC).

이 데이터셋은 GLIF 공개 보고서의 **출처가 연결된 연구 참고자료**다. 원보고서의 수치가 1차 기관에서 검증된 사실이라는 뜻이 아니며, 투자 의견은 수익을 내는 매매의 정답이 아니다. 확인된 상충 및 오류 의심 레코드는 `excluded_records.jsonl`로 격리했다. **현재 승인된 예측 학습 표본과 과거 백테스트 입력은 0개**다.

## 범위와 분석 깊이

- 공개 목록: https://glifskku.com/projects.html
- 목록 확인 18개: IM 산업보고서 11개, Market View 4개, GAA 3개.
- PDF 다운로드 18개, 총 812페이지. 접근 실패 0개.
- 18개 보고서에서 본문/표의 **선택 페이지를 분석**했다. `sources.analyzed_pages`에 검토 근거 페이지를 기록했다. 총 133개 서로 다른 보고서-페이지가 기록되며, 표지·메타데이터 확인 페이지도 포함한다.
- 전 PDF에서 디지털 텍스트를 추출·검색했고 GAA 25-2의 73페이지에는 OCR을 추가했다. 텍스트 추출이나 OCR 실행을 전 페이지 완독·전수 수치 검증으로 집계하지 않는다.
- 수치는 명시된 본문·표·그래프의 인쇄된 라벨에서만 선별했다. 선 높이·막대 길이로 정밀값을 추정하지 않았다. 내부 원장, DCF 엑셀, 실체결 로그를 확보하지 않았다.
- 직접 받은 PDF와 전체 추출 텍스트는 작업 환경의 비공개 캐시에만 두고, ZIP/Drive/저장소 배포 대상에서 제외했다. 짧은 구조화 정보와 재서술 요약만 제공한다.

## 읽는 순서와 파일 용도

1. **CODEX_CONTEXT.md**: 개발 에이전트의 입력 규칙·금지사항·추가 데이터 요구사항.
2. **README.md**: 범위·관측단위·연결·갱신 방법.
3. **data_dictionary.json**: 모든 데이터 필드의 자료형·단위·결측·키·시점 정의.
4. **quality_report.md**와 **sources.csv**: 사용 전 품질 문제와 원문 페이지·버전 확인.
5. 산업/거시/보유/성과/변경 CSV와 `research_notes.jsonl`: 연구용 자료 탐색.
6. **training_dataset.jsonl**: 검증된 예측 학습용 파일. 이번 버전은 0바이트의 빈 파일.
7. **excluded_records.jsonl**: 오류·상충 가능성 검토용 격리 자료. 학습, RAG의 사실 근거, 전략 신호, 성과 검증에서 제외한다.

Drive 업로드 도구는 0바이트 개별 파일에 `file_zero_bytes` 오류를 반환한다. 따라서 빈 `training_dataset.jsonl`은 **전체 ZIP 내부와 Economic-Daily 저장소에 0바이트로 보존**하고, Drive에는 나머지 12개 개별 파일과 전체 ZIP을 저장한다. 형식을 맞추기 위한 가짜 JSON 객체나 빈 줄을 넣지 않았다.

| 파일 | 레코드 수 |
|---|---:|
| `sources.csv` | 18 |
| `industry_metrics.csv` | 59 |
| `macro_metrics.csv` | 40 |
| `portfolio_holdings.csv` | 40 |
| `portfolio_performance.csv` | 9 |
| `portfolio_changes.csv` | 39 |
| `research_notes.jsonl` | 18 |
| `training_dataset.jsonl` | 0 |
| `excluded_records.jsonl` | 18 |

`sources.csv`는 보고서와 수집본 버전당 한 행이다. `industry_metrics.csv`는 기업/산업-기간-지표, `macro_metrics.csv`는 국가-지표-대상기간-보고된 빈티지당 한 행이다. 보유 CSV는 포트폴리오-보고서 현황표-종목/현금, 성과 CSV는 포트폴리오 또는 벤치마크-기간-성과 지표, 변경 CSV는 종목-서술 기간-행동 단위다. 같은 보고서가 여러 행의 출처라는 이유로 독립 표본 수가 늘어나는 것은 아니다.

## 읽기와 연결

모든 파일은 UTF-8이다. CSV의 중첩 배열·객체 셀은 JSON 문자열이며, 빈 셀은 결측이다. 코드의 선행 0을 보존한다. JSON은 null을 사용하며 0은 원문에 명시된 경우에만 쓴다.

```python
from pathlib import Path
import csv, json
base = Path('glif_investment_dataset')
with (base/'sources.csv').open(encoding='utf-8', newline='') as f:
    sources = {(r['source_id'], r['source_version']): r for r in csv.DictReader(f)}
with (base/'industry_metrics.csv').open(encoding='utf-8', newline='') as f:
    metrics = list(csv.DictReader(f))
for r in metrics:
    source = sources[(r['source_id'], r['source_version'])]
    pages = json.loads(r['source_pages'])  # PDF 물리 페이지, 표지=1
    value = None if r['normalized_value'] == '' else float(r['normalized_value'])
    eligible = r['training_eligible'] == 'true'  # bool('false')를 사용하지 않음
    assert not eligible
train = [json.loads(x) for x in (base/'training_dataset.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
assert train == []
```

수치 CSV의 source_id·source_version은 sources의 외부키이며 원문 페이지는 source_pages에 보존한다. `entity_id`로 기업 지표를 결합하고 포트폴리오 파일은 `portfolio_id`로 연결한다. 기준일 미확인 현황표와 특정일의 변경을 임의로 결합하지 않는다. 현재 종목 마스터는 당시의 상장 상태를 증명하지 않는다.

## 시점과 정규화

관측기간, 문서 발간일, 실제 공개시점, 현재 수집시점을 분리한다. 실제 최초 공개시각은 모두 미확인(null)이다. `available_at`은 **현재 다운로드 성공시각이라는 보수적 상한**만 뜻한다. 이 자료를 2025~2026년의 과거 의사결정 시점으로 되돌려 배치할 수 없다. 목록일·PDF 생성일·표지 날짜를 공개시각으로 대체하지 않는다.

비중과 수익률은 1=100%인 ratio, 비중 변화는 1=1%p인 percentage_point이다. 원/달러를 섞지 않으며, 한국 종목이 GAA 표에서 달러로 표시된 경우 그 달러 표기를 보존하고 환산 기준 미확인으로 표시한다. 연결/별도 미기재는 null이다. 연간·분기 관측 구간의 달력 경계 계산은 거래시점 추정이 아니다.

## 갱신과 재현

작업 위치는 요청한 Economic-Daily 저장소 체크아웃이다. 저장소의 `scripts/collect_glif.py`가 현재 공개 목록의 URL만 다운로드하고 `.cache/<UTC시각>/`에 새 수집본을 남긴다. `scripts/ocr_glif.py`는 이미지형 GAA 25-2의 OCR을 보조한다. `inputs/source_snapshot.json`·`inputs/entity_verification.json`과 `scripts/curated_records.py`는 이번 검토본의 재현 입력이다.

```bash
# 이미 검토한 이번 버전의 오프라인 재생성 (Python 3.10+)
python scripts/build_dataset.py
python scripts/validate_dataset.py
python scripts/package_dataset.py

# 새 목록/PDF 수집만 수행 (추가: PyMuPDF)
python scripts/collect_glif.py
```

새 PDF의 해시가 바뀌면 새 버전을 추가하고 원문·날짜·수치·기업 식별·이용조건을 다시 검토한다. 새 수집 결과에 기존 수동 추출값을 자동 재사용하지 않는다. `prepare_snapshot.py`는 검토 후 입력을 동결하는 도구이며, 기존 입력 덮어쓰기는 별도 버전/브랜치에서 수행한다. 예정되지 않은 반복 수집이나 자동 갱신 일정은 만들지 않았다.

## 활용 범위와 추가 데이터

현재 가능한 작업은 주·월 단위 후보 탐색, 투자 논거·위험요인 검색, 공급망 관계 검토, 자산배분·집중도·리밸런싱 가설 설계, 검증 대기 데이터의 탐색이다. 본 파일들은 개발 참고자료이며 바로 학습에 투입하는 데이터가 아니다.

예측 학습과 역사적 백테스트에는 공개시점 증거와 당시 보고서 버전, 시점별 공시, 상장/상폐·기업행사 이력, 배당·수정주가·거래량·거래일 캘린더, 환율, 거래비용, 거시 빈티지가 추가로 필요하다. 실시간 자동매매에는 **시세·호가·체결·주문·잔고 스트림과 증권사 API**가 별도로 필요하다. 보고서의 Current Price나 Average Price는 체결 데이터가 아니다.

공개 보고서라는 이유로 인용된 Bloomberg/Quantiwise/Clarksons/TrendForce 등 유료 원자료의 재배포·모델 학습 권한을 가정하지 않는다. `sources.upstream_sources`는 출처 캡션의 추적 목록이며, 각 자료의 이용조건과 인용 수치의 원출처 대조는 추가 확인 대상이다.
