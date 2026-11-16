"""Explicit field definitions shared by the writer and validator."""
FIELDS={}
def F(name,description,typ='string',unit=None,allowed=None,nullable=True,origin='source_extracted',key=None,time=None):
    FIELDS[name]=dict(name=name,description=description,data_type=typ,unit=unit,allowed_values=allowed,
        nullable=nullable,origin=origin,join_key=key,temporal_meaning=time)

F('record_id','파일 내 고유 레코드 ID','string',nullable=False,origin='assigned',key='primary key')
F('source_id','GLIF 공개 목록의 팀과 번호를 조합한 안정적 보고서 ID',nullable=False,origin='assigned',key='sources.csv.source_id')
F('source_version','수집한 PDF SHA-256 앞 16자리; source_id와 함께 버전을 식별',nullable=False,origin='calculated',key='sources.csv.(source_id,source_version)',time='수집본 버전')
F('source_pages','PDF 물리 페이지 번호의 배열; 표지=1, 인쇄 쪽번호와 다를 수 있음','array[integer]',unit='PDF page',nullable=False)
F('available_at','이 수집본에 보수적으로 부여한 이용 가능 시각. 최초 공개일 아님',typ='datetime',time='현재 PDF 다운로드 성공 시각; 이보다 앞선 특징으로 사용 금지',origin='observed')
F('collected_at','해당 출처 바이트를 수집한 시각',typ='datetime',time='현재 수집 시점',origin='observed')
F('evidence_kind','해당 값이나 요약을 확인한 원문 형식',allowed=['pdf_text','table_visual_verified','chart_printed_label_visual_verified','ocr_text_reviewed','derived'],nullable=False,origin='analyst_classification')
F('quality_status','원자료 대조 상태; report_transcription만으로 사실 검증 완료를 뜻하지 않음',allowed=['needs_primary_verification','quarantined'],nullable=False,origin='analyst_classification')
F('quality_flags','결측·상충·시점 문제를 설명하는 기계 판독 코드','array[string]',nullable=False,origin='analyst_classification')
F('review_required','외부 원출처·시점 또는 내용의 추가 확인 필요 여부','boolean',nullable=False,origin='analyst_classification')
F('training_eligible','예측 모델 입력/정답 학습 승인 여부. 이번 버전은 전부 false','boolean',nullable=False,origin='validation')
F('historical_backtest_eligible','수집 이전 시점 백테스트 사용 승인 여부. 이번 버전은 전부 false','boolean',nullable=False,origin='validation')
F('entity_id','현재 식별된 기업/종목 키. KR:코드, US:티커, NAME:미검증 이름, INDUSTRY:산업',nullable=False,origin='assigned',key='entity_id across data files; current identity only')
F('entity_name','현재 공개 종목 디렉터리의 회사/증권명 또는 보고서의 미검증 이름',origin='external_verified_or_source')
F('reported_ticker','보고서에 표기된 티커 원문. 현재 검증 티커와 구분')
F('ticker','공개 종목 디렉터리에서 현재 거래소까지 확인한 코드; 선행 0 유지',origin='external_verified',key='(ticker,exchange); historical validity unverified')
F('exchange','수집 시점 공개 디렉터리의 상장시장; 보고서 당시의 상장 이력 아님',allowed=['KOSPI','KOSDAQ','NASDAQ','NYSE','NYSE_ARCA','CBOE_BZX','NYSE_AMERICAN','IEX'],origin='external_verified')
F('country','종목 행은 상장시장 국가, 거시 행은 관측 대상 국가. 발행사 법적 소재국/매출 노출국 아님',unit='ISO 3166-1 alpha-2',origin='external_verified_or_analyst_mapping')
F('identity_source_url','종목과 거래소를 대조한 공개 디렉터리 URL',origin='external_verified')
F('identity_verified_at','현재 종목 식별을 검증한 디렉터리 수집 시각','datetime',origin='observed',time='과거 상장상태를 증명하지 않음')
F('identity_status','종목 식별 검증 수준',allowed=['current_directory_verified_historical_unverified','unverified','not_applicable'],origin='validation')
F('industry','원문 주제 기준 산업 분류; 외부 산업분류 코드 아님',origin='analyst_classification')
F('metric_name','지표 식별자. segment·growth·margin 등 서로 다른 의미를 분리',nullable=False,origin='analyst_classification')
F('observation_period','지표 대상기간. YYYY, YYYY-MM, YYYY-Qn, YYYY-Hn, YYYY-MM-DD, 월 구간 또는 원문 FY 표기',time='수치가 설명하는 기준기간; 정보 이용 가능 시점 아님')
F('observation_period_raw','정리 전 기간 표기/검토 레이블. FY 기간의 달력 경계를 확인하지 못하면 observation_period는 null',time='원문의 관측기간 의미를 보존; 원문 전체 날짜 표기는 PDF에서 확인')
F('period_start','명시된 달력 기간의 시작일. 불명확한 회계연도/상·중·하순에는 null','date',origin='calculated',time='관측구간 시작; 거래일로 간주 금지')
F('period_end','명시된 달력 기간의 종료일. 불명확한 회계연도/상·중·하순에는 null','date',origin='calculated',time='관측구간 끝; 거래일로 간주 금지')
F('period_precision','기간 해상도',allowed=['day','month','quarter','half_year','year','month_range','fiscal_unresolved','unknown','part_of_month','reported_day'],origin='analyst_classification')
F('original_value','숫자·기호·한국식 큰 단위를 포함한 원문 표기 문자열; 음수/근사/범위 의미 보존')
F('original_unit','원문 숫자를 해석하는 단위. 숫자 표기에 포함된 단위도 별도 기록')
F('normalized_value','원문 수치를 명시적 단위 변환만 적용한 값; 사실성 검증 완료 의미 아님','number',origin='calculated')
F('normalized_unit','정규화 단위. ratio는 1=100%, percentage_point는 1=1%p',origin='calculated')
F('value_kind','실적이라고 서술된 값, 추정, 전망, 회사계획, 의견을 분리',allowed=['reported_actual','estimate','forecast','company_plan','opinion','unknown','derived'],nullable=False,origin='analyst_classification')
F('value_qualifier','정확한 값/근사값/상한·하한을 분리',allowed=['exact','approximate','lower_bound','upper_bound','unknown'],origin='analyst_classification')
F('financial_statement_scope','연결·별도·부문 기준; 명시가 없으면 null',allowed=['consolidated','standalone','segment'])
F('currency','값/가격/평가금액의 표시 통화. 추정 환산 금지',unit='ISO 4217',allowed=['KRW','USD','JPY','AUD'])
F('normalization_formula','원문값을 정규화한 산식. 금융 지표 추정식과 구분',origin='calculated')
F('calculation_inputs_json','계산 입력값/원 단위/입력 record_id를 저장한 객체','object',origin='calculated')
F('upstream_source_raw','보고서가 인용한 외부 출처. 페이지 도표의 출처이면 그 범위를 명시; 미확인은 null')
F('release_date_reported','보고서가 표시한 지표 발표일. 원발표 기관에서 검증한 시각이 아님','date',time='지표 발표 날짜만 확인; 시각/시간대 미확인')
F('release_at','원발표 기관에서 검증한 지표 발표 시각. 이번 수집은 null','datetime',time='지표 원발표 시점')
F('revision_status','원문에 나타난 개정/추정 버전 설명. 알 수 없으면 null',time='지표 개정 여부와 보고서의 주장')
F('vintage_date','원발표 빈티지 날짜. 별도 원자료로 검증하지 못해 null','date',time='당시 배포된 데이터 버전')
F('measurement_basis','YoY/MoM/SAAR/수준/정책금리 구간 등 측정 의미. 확인된 수준에서만 기록',origin='analyst_classification')
F('portfolio_id','학기별 GLIF 포트폴리오 식별자; 동일 실계좌라는 뜻 아님',nullable=False,origin='assigned',key='portfolio_id across portfolio files')
F('snapshot_id','보고서 내 특정 보유 현황 표의 식별자',nullable=False,origin='assigned',key='portfolio_holdings.csv.snapshot_id')
F('as_of_date','표의 기준일. 날짜 미기재는 null; 그래프 마지막 눈금으로 대체하지 않음','date',time='포트폴리오 보유 상태 기준일')
F('period_raw','원문 기간 표현 및 근거. Early/Late/Mid 등의 표현을 정확한 날짜로 바꾸지 않음',time='포트폴리오/변경의 원문 기준기간')
F('asset_type','종목명·상품 유형에 따른 자산 분류',allowed=['equity','equity_etf','bond_etf','commodity_etf','currency_etf','cash','unknown'],origin='analyst_classification')
F('holding_status','본문/표가 명시한 보유·완전청산·현금 상태. 체결 확인 아님',allowed=['held_reported','exited_reported','cash','unconfirmed'],origin='analyst_classification')
F('average_price_raw','보고서 평균 매입가 문자열; 달러 기호 포함')
F('average_price','보고서 평균 매입가를 숫자로 파싱한 값; 실제 체결가 미확인','number',unit='currency/share',origin='parsed')
F('valuation_price_raw','보고서 Current Price 원문 문자열')
F('valuation_price','보고서 평가가격; 시세 API/체결 로그에서 검증하지 않음','number',unit='currency/share',origin='parsed')
F('market_value_raw','보고서 평가금액 문자열')
F('market_value','보고서 평가금액. 청산의 명시적 0은 결측값과 다름','number',unit='currency',origin='parsed')
F('weight_raw','보고서 비중 문자열, % 기호 포함')
F('weight_ratio','비중 원문 %/100. 1=100%','number',unit='ratio',origin='calculated')
F('return_raw','보고서 종목 수익률 문자열, % 기호 포함')
F('return_ratio','보고서 수익률 %/100. 배당/비용/거래이력 미확인','number',unit='ratio',origin='calculated')
F('return_realization','실현·미실현·혼합·미확인 구분',allowed=['realized','unrealized','mixed','unconfirmed'])
F('price_type','보고서 가격의 의미',allowed=['reported_valuation_not_execution'],nullable=False,origin='analyst_classification')
F('operation_mode','모의운용 또는 실거래 여부. 계좌 근거 없으므로 unconfirmed',allowed=['simulated','live','unconfirmed'],nullable=False)
F('price_ratio_return_check','valuation_price/average_price-1; 오류 탐지 전용. 배당·비용 반영 실제 수익률 아님','number',unit='ratio',origin='calculated')
F('performance_scope','포트폴리오 또는 벤치마크 성과',allowed=['portfolio','benchmark'],origin='analyst_classification')
F('benchmark_name','원문 비교지수 명칭. 정확한 지수 코드/총수익지수 여부 미확인')
F('is_cumulative','누적 여부; 알 수 없으면 null','boolean')
F('cost_inclusion','성과에 수수료·세금·슬리피지가 포함됐는지',allowed=['included','excluded','unconfirmed'])
F('event_date','보고서에 명시된 변경 일자; 실제 거래시점은 execution_at으로 별도 관리','date',time='보고된 변경일, 실체결일 아님')
F('execution_at','검증된 실제 체결 시각. 거래 로그 미확보로 null','datetime',time='실제 거래 시각')
F('exact_execution_time_verified','실제 거래시각 검증 여부','boolean',nullable=False,origin='validation')
F('retrospective','보고서가 과거 변경을 사후 설명하는 기록인지','boolean',nullable=False,origin='analyst_classification')
F('action','편입/확대/축소/청산/유지',allowed=['initiate','increase','reduce','exit','hold'],origin='analyst_classification')
F('weight_before_ratio','변경 전 비중. 명시되지 않으면 null','number',unit='ratio')
F('weight_after_ratio','변경 후 비중. 명시되지 않으면 null','number',unit='ratio')
F('weight_change_raw','비중 변화 원문. %p를 %와 혼동하지 않음')
F('weight_change_pp','원문 비중 변화. 1=1%p, 비율 단위가 아님','number',unit='percentage_point',origin='parsed')
F('rationale','원문 투자 근거를 요약한 텍스트; 수익 보장 또는 정답 라벨 아님',origin='analyst_paraphrase')
F('market_event','보고서가 연결한 당시 시장 사건을 요약. 원출처 사실 검증과 구분',origin='analyst_paraphrase')
F('related_entities','관련 기업·자산 이름 목록','array[string]',origin='analyst_classification')
F('related_industries','관련 산업/자산군 목록','array[string]',origin='analyst_classification')
F('summary','선택 분석 페이지의 한국어 요약. 보고서 전체 복제/전체내용 요약 아님',origin='analyst_paraphrase')
F('investment_thesis','보고서가 제시한 투자 논거 목록','array[string]',origin='analyst_paraphrase')
F('growth_catalysts','검토 페이지에서 확인한 성장 촉매. 없거나 미확인은 null','array[string]',origin='analyst_paraphrase')
F('risk_factors','검토 페이지에서 확인한 위험요인. null은 보고서 전체에 위험이 없다는 뜻 아님','array[string]',origin='analyst_paraphrase')
F('relationships','기업 관계 객체 목록; subject,object,relation,attribution. 모두 보고서 주장','array[object]',origin='analyst_paraphrase')
F('content_type','사실과 작성자 의견을 구분하는 유형. 요약은 보고서 의견으로 귀속',allowed=['report_opinion_summary'],nullable=False,origin='analyst_classification')
F('fact_claims','외부에서 독립 검증한 서술 사실 목록. 이번 버전은 null','array[string]',origin='external_verified')
F('analyst_labels','생성된 감성 등 분석 라벨. 이번 버전은 생성하지 않음','object',origin='analyst_generated')

# Report metadata fields.
F('title','공개 목록에 등록된 보고서 제목',nullable=False)
F('team','작성 팀',allowed=['IM팀','자산운용팀'],nullable=False)
F('report_type','보고서 유형',allowed=['industry','gaa','market_view'],nullable=False,origin='analyst_classification')
F('semester','공개 목록의 학기·프로젝트명',nullable=False)
F('listed_publication_date','목록 페이지에 표기된 발간일','date',time='목록의 날짜 주장; 공개시각 아님')
F('printed_publication_date','PDF에서 확인한 표기 발간일. 목록 날짜로 채우지 않음','date',time='문서 표지/본문 날짜')
F('printed_date_evidence','PDF 날짜 원문, 페이지, 상충 설명')
F('actual_publication_at','독립 증거로 확인한 최초 공개 시각. 전부 null','datetime',time='역사적 최초 공개 시점')
F('public_access_verified_at','로그인 없이 PDF 바이트를 실제 받은 시각','datetime',origin='observed',time='현재 공개 접근 확인 시점')
F('first_discovered_at','이번 파이프라인이 공개 목록에서 보고서를 처음 기록한 시각. 인터넷 최초 발견 의미 아님','datetime',origin='observed',time='이번 수집 실행의 최초 발견')
F('availability_basis','available_at을 정한 근거',allowed=['current_download_conservative_bound'],origin='validation')
F('listing_url','보고서 목록 URL',nullable=False)
F('source_url','목록에 등록된 원문 PDF URL',nullable=False)
F('final_url','다운로드 응답의 최종 URL',origin='observed')
F('listed','현재 공개 목록에 등록되어 있는지','boolean',nullable=False,origin='observed')
F('access_status','실제 접근 결과',allowed=['downloaded','failed','not_attempted'],nullable=False,origin='observed')
F('http_status','PDF 다운로드 HTTP 상태 코드','integer',origin='observed')
F('failure_reason','다운로드 실패 원인. 성공한 자료는 null',origin='observed')
F('page_count','PDF 물리 페이지 수','integer',unit='page',origin='calculated')
F('file_size_bytes','수집 PDF 바이트 길이','integer',unit='byte',origin='calculated')
F('file_sha256','PDF 전체 바이트 SHA-256',origin='calculated',key='content version fingerprint')
F('pdf_creation_at','PDF 생성 메타데이터. 실제 공개시각으로 사용 금지','datetime',time='PDF 메타데이터 주장')
F('pdf_modified_at','PDF 수정 메타데이터. 실제 수정·재공개 시각으로 확정 불가','datetime',time='PDF 메타데이터 주장')
F('pdf_dates_raw','PDF creationDate/modDate 원문 객체','object')
F('original_version_verified','발간 당시와 동일한 원본 버전인지 검증 여부','boolean',nullable=False,origin='validation')
F('analysis_status','본문 분석 범위',allowed=['selected_pages_analyzed','not_analyzed'],nullable=False,origin='observed')
F('analyzed_pages','실제 레코드·검토 근거를 확인한 PDF 페이지 목록. 모든 페이지 완독 의미 아님','array[integer]',origin='observed')
F('text_extracted_pages','비어 있지 않은 디지털 텍스트를 얻은 페이지 수. 내용 정확도 의미 아님','integer',unit='page',origin='calculated')
F('ocr_pages','OCR를 실행한 PDF 페이지 목록; OCR 출력 모두를 수치 데이터로 채택하지 않음','array[integer]',origin='observed')
F('upstream_sources','페이지에서 추출한 자료/출처/Source 캡션 목록. 원출처와 이용조건은 미검증','array[object]')
F('license_status','보고서 및 인용 원자료의 재배포·학습 이용조건 확인 상태',allowed=['not_verified_no_raw_pdf_redistribution'],nullable=False,origin='validation')

# Training schema is declared even though the delivered file has zero rows.
F('sample_id','학습 표본 고유키','string',nullable=False,origin='assigned',key='primary key')
F('feature_as_of','모든 입력이 실제 이용 가능함을 확인한 기준시각','datetime',nullable=False,origin='validated',time='특징 컷오프')
F('input_features','특징명→특징값 객체. 각 특징의 출처·시각 검증을 외부 manifest로 보장','object',nullable=False,origin='calculated')
F('target_name','실제 시장 데이터로 계산한 타깃 식별자',nullable=False,origin='calculated')
F('target_value','실제 사후 성과로 계산한 목표값','number',nullable=False,origin='calculated')
F('target_horizon','예: 20 trading sessions; 진입·종료·거래소 캘린더 정의와 연결',nullable=False,origin='defined',time='라벨 산출 구간')
F('label_available_at','목표 기간 종료와 데이터 수신이 완료된 시각','datetime',nullable=False,origin='validated',time='정답을 실제 계산할 수 있었던 최초 시각')
F('source_ids','특징/정답 출처 ID 목록. GLIF 이외 시장 데이터 출처도 등록해야 함','array[string]',nullable=False,origin='assigned',key='sources.csv.source_id')
F('split','시간순 분할 결과',allowed=['train','validation','test'],nullable=False,origin='calculated')
F('original_record_id','격리한 원래 레코드 식별자',nullable=False,origin='assigned')
F('dataset_file','원래 레코드가 들어갈 데이터 파일명',nullable=False,origin='assigned')
F('reason_codes','학습/정상 데이터셋에서 제외한 사유 코드','array[string]',nullable=False,origin='validation')
F('original_record','원문값·정규화값·계산 근거를 담은 격리 payload. dataset_file의 스키마 사용','object',nullable=False,origin='source_and_calculated')
F('release_conditions','격리 해제를 위해 필요한 독립 검증',nullable=False,origin='analyst_instruction')

COMMON='source_version available_at collected_at evidence_kind quality_status quality_flags review_required training_eligible historical_backtest_eligible'.split()
IDENTITY='entity_id entity_name reported_ticker ticker exchange country identity_source_url identity_verified_at identity_status'.split()
VALUE='metric_name observation_period observation_period_raw period_start period_end period_precision original_value original_unit normalized_value normalized_unit value_kind value_qualifier currency normalization_formula calculation_inputs_json upstream_source_raw'.split()
SCHEMAS={
 'sources.csv':('source_id source_version title team report_type semester listed_publication_date printed_publication_date printed_date_evidence actual_publication_at public_access_verified_at first_discovered_at collected_at available_at availability_basis listing_url source_url final_url listed access_status http_status failure_reason page_count file_size_bytes file_sha256 pdf_creation_at pdf_modified_at pdf_dates_raw original_version_verified analysis_status analyzed_pages text_extracted_pages ocr_pages upstream_sources license_status quality_flags training_eligible historical_backtest_eligible').split(),
 'industry_metrics.csv':['record_id','source_id','source_pages']+IDENTITY+['industry']+VALUE+['financial_statement_scope']+COMMON,
 'macro_metrics.csv':['record_id','source_id','source_pages','country']+VALUE+['measurement_basis','release_date_reported','release_at','revision_status','vintage_date']+COMMON,
 'portfolio_holdings.csv':['record_id','source_id','source_pages','portfolio_id','snapshot_id','as_of_date','period_raw']+IDENTITY+('asset_type holding_status currency average_price_raw average_price valuation_price_raw valuation_price market_value_raw market_value weight_raw weight_ratio return_raw return_ratio return_realization price_type operation_mode price_ratio_return_check normalization_formula calculation_inputs_json').split()+COMMON,
 'portfolio_performance.csv':('record_id source_id source_pages portfolio_id performance_scope benchmark_name metric_name period_raw period_start period_end original_value original_unit normalized_value normalized_unit currency is_cumulative return_realization cost_inclusion operation_mode normalization_formula calculation_inputs_json').split()+COMMON,
 'portfolio_changes.csv':['record_id','source_id','source_pages','portfolio_id','period_raw','period_precision','event_date','execution_at','exact_execution_time_verified','retrospective']+IDENTITY+('action weight_before_ratio weight_after_ratio weight_change_raw weight_change_pp rationale market_event operation_mode').split()+COMMON,
 'research_notes.jsonl':('record_id source_id source_pages related_entities related_industries summary investment_thesis growth_catalysts risk_factors relationships content_type fact_claims analyst_labels').split()+COMMON,
 'training_dataset.jsonl':('sample_id entity_id feature_as_of input_features target_name target_value target_horizon label_available_at source_ids split').split(),
 'excluded_records.jsonl':('record_id original_record_id source_id source_pages dataset_file reason_codes original_record release_conditions training_eligible').split(),
}

def dictionary(version):
    from metric_definitions import METRICS
    result={'schema_version':'1.0.0','dataset_version':version,
      'conventions':{
       'encoding':'UTF-8 without BOM','csv':'RFC4180-compatible, comma, double-quote escaping, CRLF rows, nested values as JSON strings',
       'missing':'JSON null / CSV empty; empty array only when absence is known, never zero imputation',
       'timezone':'ISO 8601 with explicit offset for timestamps; UTC storage, Asia/Seoul collection date display',
       'ratios':'5%=0.05; 1=100%; growth may exceed 1; negative returns preserved',
       'percentage_points':'5%p = 5 percentage_point, NOT 0.05 in pp fields; pp/100 only if explicitly converting to ratio change',
       'spread':'OAS given in % retained as fraction of yield; mortgage spread quoted ambiguously in % is quarantined; no silent percent/pp repair',
       'money':'억원 * 1e8 KRW; 조원 * 1e12 KRW; 억USD * 1e8 USD; trillion_USD * 1e12 USD; no FX conversion',
       'identity':'current KRX/Nasdaq directory only, no historical listing entitlement; country is listing country',
       'availability':'available_at=current successful PDF download, a conservative observed bound. actual_publication_at remains null',
       'page_numbering':'1-based physical PDF pages; printed page numbers can differ',
       'training_policy':'Only explicitly approved and verified records can become features; all delivered training_eligible=false; quarantined payloads are audit-only',
       'upstream_terms':'Public PDF availability does not license paid underlying databases; source captions have unverified terms',
       'allowed_values_null':'null in a field definition means no finite enumeration; data_type and prose constraints still apply',
      },'files':{}}
    for filename,cols in SCHEMAS.items():
        result['files'][filename]={'format':'csv' if filename.endswith('.csv') else 'jsonl',
            'observation_unit':{
             'sources.csv':'one listed report and collected PDF version',
             'industry_metrics.csv':'one entity/industry, observation period and metric',
             'macro_metrics.csv':'one country, indicator, observation period and reported vintage',
             'portfolio_holdings.csv':'one report overview snapshot and security/cash position',
             'portfolio_performance.csv':'one portfolio/benchmark, performance period and metric',
             'portfolio_changes.csv':'one security action in a reported period',
             'research_notes.jsonl':'one selected-page report opinion summary',
             'training_dataset.jsonl':'one verified point-in-time feature/market-outcome pair; currently empty',
             'excluded_records.jsonl':'one quarantined record with reason and original payload'}[filename],
            'fields':[dict(FIELDS[c]) for c in cols]}
        for field in result['files'][filename]['fields']:
            if field['name']=='metric_name':field['allowed_values']=sorted(METRICS)
            if field['name']=='normalized_value':field['unit']='see normalized_unit field'
            if field['name']=='original_value':field['unit']='see original_unit field'
    for fn,desc in [('README.md','범위, 읽는 순서, 갱신 및 한계'),('CODEX_CONTEXT.md','개발·시점 정렬·전략 검증 요구사항'),('quality_report.md','검사 결과, 결측률, 격리 및 제외 사유')]:
        result['files'][fn]={'format':'markdown','fields':[dict(name='content',description=desc,data_type='string',unit=None,allowed_values=None,nullable=False,origin='analyst_authored',join_key=None,temporal_meaning='현재 수집본 설명')]}
    result['files']['data_dictionary.json']={'format':'json','fields':[
        dict(name=k,description=v,data_type=t,unit=None,allowed_values=None,nullable=False,origin='schema_definition',join_key=None,temporal_meaning=None)
        for k,v,t in [('schema_version','스키마 버전','string'),('dataset_version','데이터셋 버전','string'),('conventions','공통 형식·단위·시점·학습 규칙','object'),('files','파일명→format/observation_unit/fields 구조. 각 field는 name,description,data_type,unit,allowed_values,nullable,origin,join_key,temporal_meaning을 가짐','object'),('nested_objects','중첩 객체의 각 하위 필드 정의','object'),('metric_catalog','metric_name→한국어 지표 정의. 값·단위·관측기간은 행별 필드와 함께 해석','object')]]}
    result['metric_catalog']=METRICS
    result['nested_objects']={
      'relationships':{'subject':'관계 주체 이름','object':'상대 기업/자산','relation':'분석자가 표준화한 관계 유형','attribution':'report_assertion_not_independently_verified'},
      'upstream_sources':{'citation_raw':'출처 캡션 텍스트','source_pages':'PDF 페이지 정수 배열','verification_status':'page_caption_only_not_primary_verified','terms_status':'unverified'},
      'pdf_dates_raw':{'creationDate':'PDF 생성 메타데이터 원문','modDate':'PDF 수정 메타데이터 원문'},
      'calculation_inputs_json':{'numeric_input':'단위 변환 전 숫자 또는 원문 표기 파싱 결과','original_unit':'원 단위','scale':'곱할 단위 배율','record_ids':'계산에 사용한 레코드 ID 배열','average_price':'단순 가격 비율 점검 입력','valuation_price':'단순 가격 비율 점검 입력','raw_return_percent':'보고된 수익률 %','raw_weight_percent':'보고된 비중 %'},
      'original_record':'dataset_file에 지정된 파일의 fields와 동일한 구조; 그 외 임의 필드 없음',
      'input_features':'표본이 없어 자유 객체 스키마만 선언; 실제 학습 도입 시 각 특징 정의와 availability 계보를 추가해야 함',
      'analyst_labels':'이번 버전은 null; 향후 라벨 생성 시 모델·기준·신뢰도 스키마 선행 필요'}
    # Nested field objects use the same required metadata as top-level fields.
    nested_types={
      'relationships':{'subject':('string',False),'object':('string',False),'relation':('string',False),'attribution':('string',False)},
      'upstream_sources':{'citation_raw':('string',False),'source_pages':('array[integer]',False),'verification_status':('string',False),'terms_status':('string',False)},
      'pdf_dates_raw':{'creationDate':('string',True),'modDate':('string',True)},
      'calculation_inputs_json':{'numeric_input':('number',True),'original_unit':('string',True),'scale':('number',True),'record_ids':('array[string]',True),
        'average_price':('number',True),'valuation_price':('number',True),'raw_return_percent':('number',True),'raw_weight_percent':('number',True)}}
    for object_name,types in nested_types.items():
        descriptions=result['nested_objects'][object_name]
        result['nested_objects'][object_name]={'fields':[dict(name=k,description=descriptions[k],data_type=t,unit=('PDF page' if k=='source_pages' else '%' if k in ['raw_return_percent','raw_weight_percent'] else None),
          allowed_values=None,nullable=nullable,origin='calculated' if object_name=='calculation_inputs_json' else 'source_extracted_or_analyst_structured',
          join_key='record_id in metric file' if k=='record_ids' else None,temporal_meaning='PDF metadata, not publication evidence' if object_name=='pdf_dates_raw' else None)
          for k,(t,nullable) in types.items()], 'optional_members':object_name=='calculation_inputs_json'}
    return result
