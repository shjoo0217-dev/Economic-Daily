# 품질 보고서

버전 2026-11-17.v1. 기준 2026-11-17T01:34:01+09:00. 여기의 품질 검사는 파싱·출처 추적·내부 일관성 검사이며 원자료 수치의 사실성에 대한 외부 감사가 아니다.

<!-- VALIDATION_STATUS -->
기계 검증: **통과**. 14,192개 assertion 검사, 키 중복 0, 스키마/외부키/날짜형식/단위 변환 오류 0. 원문 사실성·과거 공개시각 미확인은 해소되지 않았다. 재현 결과: 저장소 `validation/validation_results.json`.
<!-- /VALIDATION_STATUS -->

## 수집·분석 실적

목록 확인 **18개**, PDF 다운로드 **18개**, 본문 선택 페이지 분석 **18개**, 다운로드 실패 **0개**, PDF 총 **812페이지**다. 완독·전수 추출 18개라는 뜻이 아니다. 18개 중 IM 11개, Market View 4개, GAA 3개이며, 공개 목록을 다시 조회한 결과다.

| source_id | 제목 | PDF 페이지 | 선택 검토 페이지 수 | 목록 발간일 | PDF 확인 날짜 |
|---|---|---:|---:|---|---|
| glif_im_11 | 정유 산업보고서 | 39 | 5 | 2026-10-10 | 2026-10-09 |
| glif_im_10 | 산업용 냉각시스템 산업보고서 | 36 | 5 | 2026-10-10 | 2026-10-09 |
| glif_im_09 | 조선 산업보고서 | 36 | 4 | 2026-04-10 | 2026-04-10 |
| glif_im_08 | 전력인프라 산업보고서 | 40 | 3 | 2026-04-10 | 2026-04-10 |
| glif_im_07 | 제약&바이오 산업보고서 | 43 | 3 | 2026-01-31 | 2025-02-06 |
| glif_im_06 | 위성 산업보고서 | 33 | 3 | 2026-01-31 | 2026-01-28 |
| glif_im_05 | 방산 산업보고서 | 34 | 4 | 2025-10-10 | 2025-10-10 |
| glif_im_04 | 화장품 산업보고서 | 34 | 3 | 2025-10-10 | 2025-10-10 |
| glif_im_03 | HBM 산업보고서 | 32 | 11 | 2025-08-14 | 2025-08-14 |
| glif_im_02 | 원자력 산업보고서 | 34 | 7 | 2025-04-11 | 2025-04-11 |
| glif_im_01 | 로봇 산업보고서 | 67 | 5 | 2025-04-11 | 2025-04-11 |
| glif_am_07 | Market View | 48 | 7 | 2026-10-10 | 미확인 |
| glif_am_06 | Global Asset Allocation | 82 | 25 | 2026-06-05 | 미확인 |
| glif_am_05 | Market View | 43 | 9 | 2026-04-10 | 미확인 |
| glif_am_04 | Global Asset Allocation | 73 | 14 | 2025-12-05 | 미확인 |
| glif_am_03 | Market View | 36 | 6 | 2025-10-10 | 미확인 |
| glif_am_02 | Global Asset Allocation | 68 | 11 | 2025-06-06 | 미확인 |
| glif_am_01 | Market View | 34 | 8 | 2025-04-11 | 2025-04-11 |

## 파일별 레코드 수

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

산업 후보 62행 중 3행을 격리했다. 거시 원문 후보 42행 중 3행을 격리하고 산식/입력키가 있는 파생 스프레드 1행을 추가했다. GAA 현황표는 51개 종목·현금 행을 전사한 뒤 내부 불일치 후보를 격리했다. 격리된 행은 기본 데이터 파일에 중복 보관하지 않았다.

## 핵심 발견과 처리

1. **공개시점·버전**: 18개 모두 실제 최초 공개시각과 발간 당시 원본 버전이 미확인이다. available_at에는 현재 다운로드 성공시각만 기록했다. PDF 메타데이터가 발간일보다 늦어도 실제 수정 공개시각으로 확정하지 않았다.
2. **날짜 충돌**: 제약·바이오 표지는 2025-02-06, 본문은 2026-02-06, 목록은 2026-01-31이다. 위성 표지는 2026-01-28, 목록은 2026-01-31이다. 냉각·정유 표지는 2026-10-09, 목록은 2026-10-10이다. 원문값을 보존했으며 임의로 고치지 않았다.
3. **기업 식별**: 조선 p33 한화오션 242660은 현재 KRX의 042660과 다르다. 원문 티커를 reported_ticker, KRX 검증 코드를 ticker에 별도 기록했다. 에이피알의 KOSDAQ 표시와 BHI의 KS 접두어도 현재 KRX 시장과 불일치한다. 과거 상장시장 이력은 확보하지 않았다. 미국 ETF의 현재 거래소도 시점별 변경 가능성이 있다.
4. **GAA 25-1 수익률**: XOVR·SHV·TLT·IAU의 보고 수익률은 평가가/평균가의 단순 비율과 0.25%p 넘게 차이 난다. 배당·수수료·매매내역이 없어 어느 값이 맞는지 단정하지 않고 관련 행을 격리했다. 단순 가격 수익률을 실제 총수익률로 대체하지 않았다.
5. **GAA 25-2 현황**: IGV·TSLA·APP·RDDT·PANW·RBLX는 비중 0%인데 평가금액이 양수다. PM은 평균가와 평가가가 같지만 수익률 0.83%다. 관계를 설명할 원장이 없어 격리했다. 일부 표의 비중 합계도 다르므로 전체 계좌를 복원할 수 없다.
6. **GAA 26-1 합계·기준 차이**: p44의 시장가치와 현금 합은 $559,574, p46 총계는 $559,557로 $17 차이가 난다. p46의 실현이익 $7,513과 손실 $8,752는 순액 -$1,239이나 기재 순액은 -$1,242다. 순실현손익 행은 격리했다. 성과표 벤치마크는 S&P 500인데 일부 리밸런싱 표는 Nasdaq으로 표시되어 정확한 비교 기준이 미해결이다. 개별 회사 설명의 가격과 현황표 가격을 덮어쓰지 않았다.
7. **물가·단위**: GAA 25-1 p16의 CPI/PPI 서술·표 라벨이 상충하고, Market View 26-1 p22의 2월 CPI 2.5%는 p26 표의 2.4%와 상충한다. 해당 헤드라인 지표를 격리했다. Market View 25-1의 금리차 2.188% 표기는 %p 의미가 불명확해 격리했다. 확인된 두 금리의 차이는 별도 파생 행으로만 계산했다.
8. **기간 보존**: Market View 26-2의 Q3 물가 평균은 각주상 7~8월만 포함한다. 3분기 전체값으로 처리하지 않는다. BHI 재무지표의 대상연도는 없으므로 빈칸이다. Early/Mid/Late 기간을 임의의 월초·15일·말일로 만들지 않았다.
9. **산업 내부 상충**: 풍산 매출부문 비중의 합계 91%, LIG넥스원 수주잔고의 본문/도표 기준기간 차이를 해결하지 못해 해당 3개 행을 격리했다. 생략된 부문·기간 차이일 가능성도 있으므로 확정 오류라고 단정하지 않는다.

## 격리 목록 — 학습·일반 검색 근거에서 제외

총 **18행**. 사용자 요청에 따라 의심·상충 값을 정상 학습 후보로 남기지 않았다. 감사 목적으로만 원문값과 변환 입력을 보존한다. 각 행의 release_conditions에 재검증 요건이 있다.

| 격리 ID | 파일 | 원 ID | 원문 | 사유 |
|---|---|---|---|---|
| excluded_0001 | industry_metrics.csv | ind_0037 | glif_im_05 p31 | segment_shares_sum_91_percent_not_100 |
| excluded_0002 | industry_metrics.csv | ind_0038 | glif_im_05 p31 | segment_shares_sum_91_percent_not_100 |
| excluded_0003 | industry_metrics.csv | ind_0040 | glif_im_05 p33 | narrative_chart_period_mismatch |
| excluded_0004 | macro_metrics.csv | mac_0003 | glif_am_01 p6 | source_uses_percent_for_yield_difference |
| excluded_0005 | macro_metrics.csv | mac_0012 | glif_am_02 p16 | quarantine_cpi_ppi_narrative_table_conflict |
| excluded_0006 | macro_metrics.csv | mac_0025 | glif_am_05 p22 | quarantine_cpi_conflicts_with_same_report_p26 |
| excluded_0007 | portfolio_holdings.csv | hold_0003 | glif_am_02 p32 | reported_return_differs_from_simple_price_ratio_over_0_25pp_unresolved |
| excluded_0008 | portfolio_holdings.csv | hold_0009 | glif_am_02 p32 | reported_return_differs_from_simple_price_ratio_over_0_25pp_unresolved |
| excluded_0009 | portfolio_holdings.csv | hold_0010 | glif_am_02 p32 | reported_return_differs_from_simple_price_ratio_over_0_25pp_unresolved |
| excluded_0010 | portfolio_holdings.csv | hold_0012 | glif_am_02 p32 | reported_return_differs_from_simple_price_ratio_over_0_25pp_unresolved |
| excluded_0011 | portfolio_holdings.csv | hold_0015 | glif_am_04 p36 | positive_market_value_with_zero_weight_unresolved |
| excluded_0012 | portfolio_holdings.csv | hold_0018 | glif_am_04 p36 | positive_market_value_with_zero_weight_unresolved |
| excluded_0013 | portfolio_holdings.csv | hold_0019 | glif_am_04 p36 | positive_market_value_with_zero_weight_unresolved |
| excluded_0014 | portfolio_holdings.csv | hold_0022 | glif_am_04 p36 | positive_market_value_with_zero_weight_unresolved |
| excluded_0015 | portfolio_holdings.csv | hold_0023 | glif_am_04 p36 | positive_market_value_with_zero_weight_unresolved |
| excluded_0016 | portfolio_holdings.csv | hold_0024 | glif_am_04 p36 | positive_market_value_with_zero_weight_unresolved |
| excluded_0017 | portfolio_holdings.csv | hold_0029 | glif_am_04 p36 | reported_return_differs_from_simple_price_ratio_over_0_25pp_unresolved |
| excluded_0018 | portfolio_performance.csv | perf_0010 | glif_am_06 p46 | reported_net_realized_pnl_minus1242_vs_components_minus1239 |

## OCR·원문 숫자 검토

GAA 25-2는 73페이지 중 디지털 텍스트가 비어 있지 않은 페이지가 10개뿐이었다. 전체 73페이지에 Tesseract 영어 OCR을 수행했다. 현황표 p36은 렌더링 이미지로 티커·숫자·부호를 대조했다. OCR은 IAU/1AU, 마이너스 부호, 17.75/7.75 등을 잘못 읽을 수 있어 OCR 출력 자체를 자동 수치화하지 않았다. p59·p63의 비중 변화는 부호/숫자 검토를 완료하지 못해 추출하지 않았다. 원문 서술에서 식별한 행동만 review_required=true로 기록했다.

GAA 25-1 p32, GAA 26-1 p44, 제약·바이오 표지 p1, 한화오션 코드 p33도 렌더링 이미지로 확인했다. IM 일부 글꼴은 제목이 반복 음절로 깨지고, 원자력 PDF는 중복 텍스트·좌표 같은 숫자가 섞인다. 디지털 텍스트 수치 104개 후보의 원문 문자열 존재 검사를 수행했지만 문자열 일치는 수치의 사실성을 보장하지 않는다. 주요 표의 시각 검토도 원자료가 맞다는 검증과 다르다.

## 파일 전달 제한

Drive 업로드 도구가 0바이트 개별 파일을 `file_zero_bytes`로 거부했다. 빈 학습 파일은 전체 ZIP 안과 저장소에 정확히 0바이트로 보존한다. Drive 폴더에는 이 파일을 포함한 전체 ZIP과 나머지 12개 개별 파일을 저장한다. 다른 데이터나 빈 줄로 학습 파일을 채우지 않는다.

## 결측·중복·단위·날짜

아래 결측률은 JSON null/CSV 빈칸만 센다. 보고된 0이나 알려진 빈 목록은 결측이 아니다. 값이 없는 학습 파일의 결측률은 N/A다. 핵심 미확인은 전체 최초 공개시각·원버전, 모든 실제 체결시각과 실거래 여부, 다수 연결/별도 기준과 원자료 인용 범위다. 검증 스크립트는 필드명/형식/UTF-8/JSONL 객체/소스 FK/페이지 범위/키 중복/유효 날짜/타임존/비중 범위/정규화 산식/격리 배제/빈 학습 파일을 검사한다. 결과는 위 기계 검증 상태에 반영된다.

## 학습·백테스트에서 제외한 범위와 추가 확보

**18개 모든 보고서 버전이 과거 백테스트와 예측 학습에서 제외**된다. 이유는 최초 공개시점과 당시 버전 미확인, 1차 출처 수치 미검증, 독립적인 미래 가격 라벨 부재, 거래비용·기업행사·기간 종료 검증 부재다. 39개 리밸런싱 행은 모두 사후 서술이며 실체결 증거가 없다. 연구 요약 18개도 저자가 제시한 의견이며 사실·정답 라벨이 아니다.

증권사 API, Open DART, FRED/ALFRED 문서에 공개 접근했지만 인증키/계약을 사용하는 시장·공시·거시 데이터셋을 수집하지 않았다. 확보한 외부 데이터는 공개 KRX/Nasdaq 종목 디렉터리의 현재 식별 증거뿐이다. 필요한 추가 자료는 당시 공개 로그·보존된 PDF 버전, 지표 발표시각과 수정 이력, 수정 OHLCV·배당·기업행사·상폐 이력, 거래일 캘린더, 환율, 시세·호가·체결 스트림, 수수료·세금·슬리피지 자료, 계좌·거래 로그다. 각 공급자의 재배포·학습 이용조건도 확인해야 한다.

학기·방학 단위의 비정기 자료 18개, GAA 포트폴리오 3개만으로 주·월 단위 연속 투자 유니버스나 충분한 독립 학습 표본이 형성되지 않는다. 동일 보고서 내 여러 지표는 강하게 의존하며, 종목 추천과 성과의 선택편향도 있다. 결측·격리 이후 보유표는 완결된 계좌 스냅샷이 아니다.

## 필드별 결측률

### sources.csv

| 필드 | 결측 수 | 결측률 |
|---|---:|---:|
| source_id | 0 | 0.00% |
| source_version | 0 | 0.00% |
| title | 0 | 0.00% |
| team | 0 | 0.00% |
| report_type | 0 | 0.00% |
| semester | 0 | 0.00% |
| listed_publication_date | 0 | 0.00% |
| printed_publication_date | 6 | 33.33% |
| printed_date_evidence | 0 | 0.00% |
| actual_publication_at | 18 | 100.00% |
| public_access_verified_at | 0 | 0.00% |
| first_discovered_at | 0 | 0.00% |
| collected_at | 0 | 0.00% |
| available_at | 0 | 0.00% |
| availability_basis | 0 | 0.00% |
| listing_url | 0 | 0.00% |
| source_url | 0 | 0.00% |
| final_url | 0 | 0.00% |
| listed | 0 | 0.00% |
| access_status | 0 | 0.00% |
| http_status | 0 | 0.00% |
| failure_reason | 18 | 100.00% |
| page_count | 0 | 0.00% |
| file_size_bytes | 0 | 0.00% |
| file_sha256 | 0 | 0.00% |
| pdf_creation_at | 0 | 0.00% |
| pdf_modified_at | 0 | 0.00% |
| pdf_dates_raw | 0 | 0.00% |
| original_version_verified | 0 | 0.00% |
| analysis_status | 0 | 0.00% |
| analyzed_pages | 0 | 0.00% |
| text_extracted_pages | 0 | 0.00% |
| ocr_pages | 0 | 0.00% |
| upstream_sources | 0 | 0.00% |
| license_status | 0 | 0.00% |
| quality_flags | 0 | 0.00% |
| training_eligible | 0 | 0.00% |
| historical_backtest_eligible | 0 | 0.00% |
### industry_metrics.csv

| 필드 | 결측 수 | 결측률 |
|---|---:|---:|
| record_id | 0 | 0.00% |
| source_id | 0 | 0.00% |
| source_pages | 0 | 0.00% |
| entity_id | 0 | 0.00% |
| entity_name | 0 | 0.00% |
| reported_ticker | 17 | 28.81% |
| ticker | 6 | 10.17% |
| exchange | 6 | 10.17% |
| country | 6 | 10.17% |
| identity_source_url | 6 | 10.17% |
| identity_verified_at | 6 | 10.17% |
| identity_status | 0 | 0.00% |
| industry | 0 | 0.00% |
| metric_name | 0 | 0.00% |
| observation_period | 10 | 16.95% |
| observation_period_raw | 9 | 15.25% |
| period_start | 10 | 16.95% |
| period_end | 10 | 16.95% |
| period_precision | 0 | 0.00% |
| original_value | 0 | 0.00% |
| original_unit | 0 | 0.00% |
| normalized_value | 0 | 0.00% |
| normalized_unit | 0 | 0.00% |
| value_kind | 0 | 0.00% |
| value_qualifier | 0 | 0.00% |
| currency | 27 | 45.76% |
| normalization_formula | 0 | 0.00% |
| calculation_inputs_json | 0 | 0.00% |
| upstream_source_raw | 52 | 88.14% |
| financial_statement_scope | 48 | 81.36% |
| source_version | 0 | 0.00% |
| available_at | 0 | 0.00% |
| collected_at | 0 | 0.00% |
| evidence_kind | 0 | 0.00% |
| quality_status | 0 | 0.00% |
| quality_flags | 0 | 0.00% |
| review_required | 0 | 0.00% |
| training_eligible | 0 | 0.00% |
| historical_backtest_eligible | 0 | 0.00% |
### macro_metrics.csv

| 필드 | 결측 수 | 결측률 |
|---|---:|---:|
| record_id | 0 | 0.00% |
| source_id | 0 | 0.00% |
| source_pages | 0 | 0.00% |
| country | 0 | 0.00% |
| metric_name | 0 | 0.00% |
| observation_period | 2 | 5.00% |
| observation_period_raw | 2 | 5.00% |
| period_start | 2 | 5.00% |
| period_end | 2 | 5.00% |
| period_precision | 0 | 0.00% |
| original_value | 1 | 2.50% |
| original_unit | 1 | 2.50% |
| normalized_value | 0 | 0.00% |
| normalized_unit | 0 | 0.00% |
| value_kind | 0 | 0.00% |
| value_qualifier | 0 | 0.00% |
| currency | 38 | 95.00% |
| normalization_formula | 0 | 0.00% |
| calculation_inputs_json | 0 | 0.00% |
| upstream_source_raw | 11 | 27.50% |
| measurement_basis | 0 | 0.00% |
| release_date_reported | 34 | 85.00% |
| release_at | 40 | 100.00% |
| revision_status | 36 | 90.00% |
| vintage_date | 40 | 100.00% |
| source_version | 0 | 0.00% |
| available_at | 0 | 0.00% |
| collected_at | 0 | 0.00% |
| evidence_kind | 0 | 0.00% |
| quality_status | 0 | 0.00% |
| quality_flags | 0 | 0.00% |
| review_required | 0 | 0.00% |
| training_eligible | 0 | 0.00% |
| historical_backtest_eligible | 0 | 0.00% |
### portfolio_holdings.csv

| 필드 | 결측 수 | 결측률 |
|---|---:|---:|
| record_id | 0 | 0.00% |
| source_id | 0 | 0.00% |
| source_pages | 0 | 0.00% |
| portfolio_id | 0 | 0.00% |
| snapshot_id | 0 | 0.00% |
| as_of_date | 23 | 57.50% |
| period_raw | 0 | 0.00% |
| entity_id | 0 | 0.00% |
| entity_name | 0 | 0.00% |
| reported_ticker | 0 | 0.00% |
| ticker | 3 | 7.50% |
| exchange | 3 | 7.50% |
| country | 3 | 7.50% |
| identity_source_url | 3 | 7.50% |
| identity_verified_at | 3 | 7.50% |
| identity_status | 0 | 0.00% |
| asset_type | 0 | 0.00% |
| holding_status | 0 | 0.00% |
| currency | 0 | 0.00% |
| average_price_raw | 3 | 7.50% |
| average_price | 3 | 7.50% |
| valuation_price_raw | 3 | 7.50% |
| valuation_price | 3 | 7.50% |
| market_value_raw | 0 | 0.00% |
| market_value | 0 | 0.00% |
| weight_raw | 1 | 2.50% |
| weight_ratio | 1 | 2.50% |
| return_raw | 3 | 7.50% |
| return_ratio | 3 | 7.50% |
| return_realization | 0 | 0.00% |
| price_type | 0 | 0.00% |
| operation_mode | 0 | 0.00% |
| price_ratio_return_check | 3 | 7.50% |
| normalization_formula | 0 | 0.00% |
| calculation_inputs_json | 0 | 0.00% |
| source_version | 0 | 0.00% |
| available_at | 0 | 0.00% |
| collected_at | 0 | 0.00% |
| evidence_kind | 0 | 0.00% |
| quality_status | 0 | 0.00% |
| quality_flags | 0 | 0.00% |
| review_required | 0 | 0.00% |
| training_eligible | 0 | 0.00% |
| historical_backtest_eligible | 0 | 0.00% |
### portfolio_performance.csv

| 필드 | 결측 수 | 결측률 |
|---|---:|---:|
| record_id | 0 | 0.00% |
| source_id | 0 | 0.00% |
| source_pages | 0 | 0.00% |
| portfolio_id | 0 | 0.00% |
| performance_scope | 0 | 0.00% |
| benchmark_name | 6 | 66.67% |
| metric_name | 0 | 0.00% |
| period_raw | 0 | 0.00% |
| period_start | 7 | 77.78% |
| period_end | 7 | 77.78% |
| original_value | 0 | 0.00% |
| original_unit | 0 | 0.00% |
| normalized_value | 0 | 0.00% |
| normalized_unit | 0 | 0.00% |
| currency | 6 | 66.67% |
| is_cumulative | 3 | 33.33% |
| return_realization | 0 | 0.00% |
| cost_inclusion | 0 | 0.00% |
| operation_mode | 0 | 0.00% |
| normalization_formula | 0 | 0.00% |
| calculation_inputs_json | 0 | 0.00% |
| source_version | 0 | 0.00% |
| available_at | 0 | 0.00% |
| collected_at | 0 | 0.00% |
| evidence_kind | 0 | 0.00% |
| quality_status | 0 | 0.00% |
| quality_flags | 0 | 0.00% |
| review_required | 0 | 0.00% |
| training_eligible | 0 | 0.00% |
| historical_backtest_eligible | 0 | 0.00% |
### portfolio_changes.csv

| 필드 | 결측 수 | 결측률 |
|---|---:|---:|
| record_id | 0 | 0.00% |
| source_id | 0 | 0.00% |
| source_pages | 0 | 0.00% |
| portfolio_id | 0 | 0.00% |
| period_raw | 0 | 0.00% |
| period_precision | 0 | 0.00% |
| event_date | 35 | 89.74% |
| execution_at | 39 | 100.00% |
| exact_execution_time_verified | 0 | 0.00% |
| retrospective | 0 | 0.00% |
| entity_id | 0 | 0.00% |
| entity_name | 0 | 0.00% |
| reported_ticker | 0 | 0.00% |
| ticker | 0 | 0.00% |
| exchange | 0 | 0.00% |
| country | 0 | 0.00% |
| identity_source_url | 0 | 0.00% |
| identity_verified_at | 0 | 0.00% |
| identity_status | 0 | 0.00% |
| action | 0 | 0.00% |
| weight_before_ratio | 39 | 100.00% |
| weight_after_ratio | 39 | 100.00% |
| weight_change_raw | 11 | 28.21% |
| weight_change_pp | 11 | 28.21% |
| rationale | 0 | 0.00% |
| market_event | 0 | 0.00% |
| operation_mode | 0 | 0.00% |
| source_version | 0 | 0.00% |
| available_at | 0 | 0.00% |
| collected_at | 0 | 0.00% |
| evidence_kind | 0 | 0.00% |
| quality_status | 0 | 0.00% |
| quality_flags | 0 | 0.00% |
| review_required | 0 | 0.00% |
| training_eligible | 0 | 0.00% |
| historical_backtest_eligible | 0 | 0.00% |
### research_notes.jsonl

| 필드 | 결측 수 | 결측률 |
|---|---:|---:|
| record_id | 0 | 0.00% |
| source_id | 0 | 0.00% |
| source_pages | 0 | 0.00% |
| related_entities | 0 | 0.00% |
| related_industries | 0 | 0.00% |
| summary | 0 | 0.00% |
| investment_thesis | 0 | 0.00% |
| growth_catalysts | 1 | 5.56% |
| risk_factors | 7 | 38.89% |
| relationships | 9 | 50.00% |
| content_type | 0 | 0.00% |
| fact_claims | 18 | 100.00% |
| analyst_labels | 18 | 100.00% |
| source_version | 0 | 0.00% |
| available_at | 0 | 0.00% |
| collected_at | 0 | 0.00% |
| evidence_kind | 0 | 0.00% |
| quality_status | 0 | 0.00% |
| quality_flags | 0 | 0.00% |
| review_required | 0 | 0.00% |
| training_eligible | 0 | 0.00% |
| historical_backtest_eligible | 0 | 0.00% |
### training_dataset.jsonl

0행. 결측률은 산출 불가(N/A)이며 0%로 표시하지 않음.

### excluded_records.jsonl

| 필드 | 결측 수 | 결측률 |
|---|---:|---:|
| record_id | 0 | 0.00% |
| original_record_id | 0 | 0.00% |
| source_id | 0 | 0.00% |
| source_pages | 0 | 0.00% |
| dataset_file | 0 | 0.00% |
| reason_codes | 0 | 0.00% |
| original_record | 0 | 0.00% |
| release_conditions | 0 | 0.00% |
| training_eligible | 0 | 0.00% |
