"""Selected-page curation. Report assertions are NOT independently verified facts.

Numbers are transcribed from explicit text/tables, never interpolated from curves.
The build records unit transformations and quarantines conflicts.
"""
INDUSTRY=[]
MACRO=[]
NOTES=[]
CHANGES=[]

def I(s,p,e,sector,metric,period,raw,n,u,kind='reported_actual',qual='exact',scope=None,cited=None,flags=None):
    INDUSTRY.append(dict(source_id=f'glif_im_{s:02}',source_pages=[p],entity_id=e,industry=sector,
        metric_name=metric,observation_period=period,original_value=raw,numeric_input=n,original_unit=u,
        value_kind=kind,value_qualifier=qual,financial_statement_scope=scope,
        upstream_source_raw=cited,quality_flags=flags or []))

# Long-format corporate and industry observations; units are deliberately explicit.
I(11,34,'KR:078930','정유','operating_profit','2026-H1','2조9,760억원',29760,'억원',scope='consolidated',cited='GS (p34 chart caption; assertion-level attribution not established)')
I(11,34,'KR:078930','정유','operating_profit','2026-Q2','1조7,174억원',17174,'억원',scope='consolidated',cited='GS (p34 chart caption)')
I(11,34,'KR:078930','정유','operating_profit_growth_yoy','2026-H1','130.8%',130.8,'%')
I(11,34,'NAME:GS칼텍스','정유','refining_capacity',None,'하루80만배럴',800000,'barrel/day',flags=['observation_period_unknown'])
I(11,36,'KR:010950','정유','capex','2026','약2.1조원',2.1,'조원','forecast','approximate',cited='S-OIL (p36 chart caption)')
I(11,36,'KR:010950','정유','capex','2027','약0.5조원',0.5,'조원','forecast','approximate',cited='S-OIL (p36 chart caption)')
I(11,38,'KR:096770','정유','operating_profit','2026-H1','5.6조원',5.6,'조원',scope='consolidated')
I(11,38,'KR:096770','정유','refining_capacity',None,'일111.5만배럴',1115000,'barrel/day',flags=['observation_period_unknown'])
I(10,32,'KR:011930','산업용 냉각시스템','revenue','2026-Q2','2,018억원',2018,'억원',scope='consolidated')
I(10,32,'KR:011930','산업용 냉각시스템','operating_profit','2026-Q2','31억원',31,'억원',scope='consolidated')
I(10,32,'KR:011930','산업용 냉각시스템','revenue_growth_yoy','2026-Q2','+44%',44,'%')
I(10,32,'KR:011930','산업용 냉각시스템','eng_segment_order_backlog','2026-06','3,926억원',3926,'억원',scope='segment')
I(10,35,'US:VRT','산업용 냉각시스템','order_backlog','2025-Q4','150억달러',150,'억USD')
I(10,35,'US:VRT','산업용 냉각시스템','organic_order_growth_yoy','2025-Q4','252%',252,'%')
I(10,35,'US:VRT','산업용 냉각시스템','book_to_bill_ratio','2025-Q4','약2.9배',2.9,'multiple',qual='approximate')
I(9,31,'KR:010140','조선','flng_market_share',None,'약70% 이상',70,'%','estimate','lower_bound',flags=['denominator_and_period_unclear'])
I(9,33,'KR:042660','조선','special_vessel_addressable_market',None,'1,920억달러',1920,'억USD','estimate',cited='한화오션, 언론종합, GLIF Research (page captions)',flags=['report_ticker_mismatch_242660_vs_042660','observation_period_unknown'])
I(9,35,'KR:439260','조선','suezmax_required_additional_orders',None,'134척',134,'vessel','estimate',cited='Clarksons, Okeanis Eco Tankers, GLIF Research (page captions)',flags=['observation_period_unknown'])
I(8,38,'KR:267260','전력인프라','revenue','2025-Q4','1조1,632억원',11632,'억원')
I(8,38,'KR:267260','전력인프라','operating_profit','2025-Q4','3,209억원',3209,'억원')
I(8,38,'KR:267260','전력인프라','operating_margin','2025-Q4','27.6%',27.6,'%')
I(8,38,'KR:267260','전력인프라','operating_margin_change_yoy','2025-Q4','7.2%p',7.2,'%p')
I(8,38,'KR:267260','전력인프라','revenue','2025','4조795억원',40795,'억원')
I(8,38,'KR:267260','전력인프라','operating_profit','2025','9,953억원',9953,'억원')
I(8,38,'KR:267260','전력인프라','revenue_guidance','2026','4조3,500억원',43500,'억원','company_plan')
I(8,39,'KR:103590','전력인프라','revenue','2025','2조446억원',20446,'억원',scope='consolidated')
I(8,39,'KR:103590','전력인프라','operating_profit','2025','1,512억원',1512,'억원',scope='consolidated')
I(7,35,'KR:207940','제약·바이오','ebitda_margin','2025','55%',55,'%','forecast',flags=['source_publication_date_conflict'])
I(7,35,'KR:207940','제약·바이오','revenue_growth_yoy','2025','24.4%',24.4,'%','forecast',flags=['source_publication_date_conflict'])
I(7,35,'KR:207940','제약·바이오','planned_bioreactor_capacity','2027','964,000리터',964000,'litre','company_plan',flags=['source_publication_date_conflict'])
I(6,31,'KR:189300','위성','terrestrial_antenna_revenue','2025-Q3','400억원',400,'억원',scope='segment')
I(6,31,'KR:189300','위성','terrestrial_antenna_revenue_growth_yoy','2025-Q3','25.7%',25.7,'%')
I(6,31,'KR:189300','위성','maritime_antenna_revenue_growth_yoy','2025-Q3','30.9%',30.9,'%')
I(6,31,'KR:189300','위성','ast_spacemobile_contract_value','2025-08','281억원',281,'억원')
I(6,28,'US:RKLB','위성','space_systems_revenue_share',None,'약70%',70,'%','reported_actual','approximate',flags=['observation_period_unknown'])
I(5,29,'KR:012450','방산','planned_overseas_defense_investment',None,'6조2,700억원',62700,'억원','company_plan',flags=['completion_period_unknown'])
I(5,31,'KR:103140','방산','defense_revenue_share','2025-H1','29.9%',29.9,'%',scope='segment',cited='풍산, 산업자료, GLIF Research (page captions)',flags=['segment_shares_sum_91_percent_not_100'])
I(5,31,'KR:103140','방산','copper_revenue_share','2025-H1','61.1%',61.1,'%',scope='segment',cited='풍산, 산업자료, GLIF Research (page captions)',flags=['segment_shares_sum_91_percent_not_100'])
I(5,33,'KR:079550','방산','export_revenue_share','2025-Q2','17.3%',17.3,'%',cited='LIG넥스원; DART (page captions)')
I(5,33,'KR:079550','방산','order_backlog','2025-Q3','18조3904억원',183904,'억원',cited='DART (page chart; narrative period differs from chart last quarter)',flags=['narrative_chart_period_mismatch'])
I(4,31,'KR:192820','화장품','revenue','2025-Q3','6,027억원',6027,'억원','forecast')
I(4,31,'KR:192820','화장품','operating_profit','2025-Q3','577억원',577,'억원','forecast')
I(4,31,'KR:192820','화장품','operating_margin','2025-Q3','9.6%',9.6,'%','forecast')
I(4,30,'KR:278470','화장품','japan_device_revenue_growth_yoy','2025-H1','+232%',232,'%',flags=['report_exchange_mismatch_KOSDAQ_vs_KOSPI'])
I(3,28,'KR:000660','HBM','revenue','2025-Q2','22.2조원',22.2,'조원')
I(3,28,'KR:000660','HBM','operating_profit','2025-Q2','9.2조원',9.2,'조원')
I(3,28,'KR:000660','HBM','revenue','2025-Q3','23조원',23,'조원','forecast')
I(3,28,'KR:000660','HBM','operating_profit','2025-Q3','10조원이상',10,'조원','forecast','lower_bound')
I(3,28,'KR:000660','HBM','hbm_revenue','2026','40.3조원',40.3,'조원','forecast',scope='segment')
I(3,29,'INDUSTRY:HBM','HBM','market_size','2026','591억달러',591,'억USD','forecast')
I(3,29,'INDUSTRY:HBM','HBM','supply_growth_yoy','2026','+62%YoY',62,'%','forecast')
I(3,29,'INDUSTRY:HBM','HBM','demand_growth_yoy','2026','+52%YoY',52,'%','forecast')
I(3,30,'KR:042700','HBM','revenue','2025-Q2','1,801억원',1801,'억원')
I(3,30,'KR:042700','HBM','operating_profit','2025-Q2','863억원',863,'억원')
I(3,30,'KR:042700','HBM','operating_margin','2025-Q2','47.9%',47.9,'%')
I(3,31,'KR:095340','HBM','test_socket_revenue_share','2024','95.2%',95.2,'%',scope='segment')
I(2,33,'KR:083650','원자력','revenue',None,'4047억원',4047,'억원',kind='unknown',flags=['financial_period_not_stated','report_market_prefix_KS_conflicts_with_KOSDAQ'])
I(2,33,'KR:083650','원자력','operating_profit',None,'219억원',219,'억원',kind='unknown',flags=['financial_period_not_stated','report_market_prefix_KS_conflicts_with_KOSDAQ'])
I(1,64,'NAME:FANUC','로봇','china_robot_revenue_share','FY2Q24','약26.3%',26.3,'%','reported_actual','approximate',flags=['fiscal_period_boundaries_unverified','security_identity_unverified'])
I(1,65,'NAME:Leader Drive','로봇','harmonic_drive_market_share','2021','18%',18,'%','estimate',flags=['security_identity_unverified'])
I(1,66,'US:TSLA','로봇','vehicle_production','2025-Q1','362,615대',362615,'vehicle')
I(1,66,'US:TSLA','로봇','vehicle_deliveries','2025-Q1','336,681대',336681,'vehicle')

def M(s,p,metric,period,raw,n,u='%',kind='reported_actual',cited=None,release=None,revision=None,flags=None,qual='exact'):
    MACRO.append(dict(source_id=f'glif_am_{s:02}',source_pages=[p],country='US',metric_name=metric,
        observation_period=period,original_value=raw,numeric_input=n,original_unit=u,value_kind=kind,
        value_qualifier=qual,upstream_source_raw=cited,release_date_reported=release,revision_status=revision,
        quality_flags=flags or []))
M(1,5,'mortgage_rate_30y','2025-04-10','6.62%',6.62,cited='FRED')
M(1,6,'treasury_yield_10y','2025-04-10','4.432%',4.432,cited='Investing.com (attribution on p5)')
M(1,6,'mortgage_treasury_spread','2025-04-10','2.188%',2.188,cited='FRED; Investing.com',flags=['source_uses_percent_for_yield_difference'])
M(1,11,'nonfarm_payroll_change','2025-03','22.8만명',22.8,'만명')
M(1,11,'unemployment_rate','2025-03','4.2%',4.2)
M(1,11,'labor_force_participation','2025-03','62.5%',62.5)
M(1,11,'u6_unemployment_rate','2025-03','7.9%',7.9)
M(1,12,'pce_inflation_yoy','2025-02','2.5%',2.5)
M(2,13,'unemployment_rate','2025-04','4.2%',4.2,cited='Investing.com',release='2025-05-02')
M(2,13,'nonfarm_payroll_change','2025-04','177K',177,'thousand_person',cited='Investing.com',release='2025-05-02')
M(2,13,'labor_force_participation','2025-04','62.6%',62.6,cited='Investing.com (page caption)')
M(2,16,'cpi_inflation_yoy','2025-04','3.5%',3.5,cited='Investing.com (page captions)',flags=['quarantine_cpi_ppi_narrative_table_conflict'])
M(2,21,'real_gdp_growth_saar','2025-Q2','+4.6%',4.6,kind='forecast',cited='Federal Reserve Bank of Atlanta, GDPNow',revision='GDPNow estimate as of 2025-06-02',flags=['model_estimate_not_realized_gdp'])
M(2,21,'net_exports_gdp_growth_contribution','2025-Q2','+1.45%p',1.45,'%p','forecast',cited='Federal Reserve Bank of Atlanta, GDPNow',revision='GDPNow estimate as of 2025-06-02')
M(3,11,'mortgage_rate_30y','2025-10-02','6.34%',6.34,cited='FRED')
M(3,11,'treasury_yield_10y','2025-10-02','4.1%',4.1,cited='FRED')
M(3,17,'policy_rate_lower','2025-09','4.00%',4.00,cited='FOMC (report narrative)')
M(3,17,'policy_rate_upper','2025-09','4.25%',4.25,cited='FOMC (report narrative)')
M(3,20,'cpi_inflation_yoy','2025-08','2.9%',2.9)
M(3,20,'cpi_inflation_mom','2025-08','0.4%',0.4)
M(5,19,'nonfarm_payroll_change',None,'178K',178,'thousand_person',cited='Investing.com',release='2026-04-03',flags=['table_has_release_date_but_observation_month_not_stated'])
M(5,19,'unemployment_rate',None,'4.3%',4.3,cited='Investing.com',release='2026-04-03',flags=['table_has_release_date_but_observation_month_not_stated'])
M(5,20,'policy_rate_lower','2026-03','3.50%',3.5,cited='FOMC (report narrative)')
M(5,20,'policy_rate_upper','2026-03','3.75%',3.75,cited='FOMC (report narrative)')
M(5,22,'cpi_inflation_yoy','2026-02','2.5%',2.5,cited='FRED (page caption)',flags=['quarantine_cpi_conflicts_with_same_report_p26'])
M(5,22,'core_cpi_inflation_yoy','2026-02','2.5%',2.5,cited='FRED (page caption)',flags=['same_page_headline_cpi_conflict_requires_primary_check'])
M(6,4,'commercial_bank_loans_outstanding','2026','approximately $13.53 trillion',13.53,'trillion_USD',cited='FRED (page caption)',qual='approximate')
M(6,4,'commercial_industrial_loan_change','2025-H1','declined 5.6%',-5.6,'%',cited='FRED (page caption)',flags=['growth_comparison_basis_not_stated'])
M(6,14,'household_debt_delinquency_rate','2025-Q4','4.8%',4.8)
M(6,81,'labor_productivity_growth_saar','2026-Q1','0.8%',0.8)
M(6,81,'hourly_compensation_growth_saar','2026-Q1','3.1%',3.1,flags=['annualization_inferred_from_adjacent_productivity_sentence'])
M(7,9,'bb_option_adjusted_spread','2026-10-01','2.04%',2.04,cited='FRED',flags=['spread_in_percent_of_yield_not_percent_change'])
M(7,9,'b_option_adjusted_spread','2026-10-01','3.29%',3.29,cited='FRED',flags=['spread_in_percent_of_yield_not_percent_change'])
M(7,9,'ccc_lower_option_adjusted_spread','2026-10-01','12.15%',12.15,cited='FRED',flags=['spread_in_percent_of_yield_not_percent_change'])
M(7,12,'bank_loans_to_ndfi','2026-09','약2.07조달러',2.07,'trillion_USD',qual='approximate')
M(7,20,'cpi_inflation_yoy_quarter_average','2026-Q2','3.83%',3.83,cited='Investing.com; FRED')
M(7,20,'cpi_inflation_yoy_partial_quarter_average','2026-07/2026-08','3.40%',3.4,cited='Investing.com; FRED',flags=['Q3_label_is_July_August_only'])
M(7,20,'core_cpi_inflation_yoy_partial_quarter_average','2026-07/2026-08','2.45%',2.45,cited='Investing.com; FRED',flags=['Q3_label_is_July_August_only'])
M(7,20,'ppi_inflation_yoy_partial_quarter_average','2026-07/2026-08','5.10%',5.1,cited='Investing.com; FRED',flags=['Q3_label_is_July_August_only'])
M(7,30,'real_gdp_growth_saar','2026-Q1','2.5%',2.5,cited='BEA; FRED',release='2026-09-30',revision='annual revision reported for 2026-09-30; vintage not retrieved')
M(7,30,'real_gdp_growth_saar','2026-Q2','2.2%',2.2,cited='BEA; FRED',release='2026-09-30',revision='annual revision reported for 2026-09-30; vintage not retrieved')
M(7,30,'real_gdp_growth_forecast','2027','2.2%',2.2,kind='forecast',cited='IMF July update (reported; underlying release not retrieved)')

# Values from overview tables. Preserve decimal spellings and separate currencies.
# ticker | average price | reported valuation price | market value | return % | weight %
HOLDINGS={
 'glif_am_02':dict(page=32,as_of=None,period_raw='보고서 p32 현황; 그래프 눈금 4-Feb~4-Jun, 표 기준일 명시 없음',rows='''
SMH|238.32|251.30|27391.70|5.44|25.77
IGV|101.82|104.68|27740.20|2.81|26.09
XOVR|18.87|18.08|3814.88|4.19|3.59
EWJV|33.23|34.82|4282.86|4.77|4.03
TSLA|383.68|284.70|2847.00|-25.80|2.68
APP|338.65|414.14|8282.80|22.29|7.79
PLTR|83.74|119.91|7074.69|43.19|6.65
NVDA|115.79|139.99|6299.55|20.90|5.93
SHV|110.15|110.12|7708.40|7.25|7.25
TLT|84.72|86.45|2766.40|2.60|2.60
FXY|62.33|64.10|3140.90|2.95|2.95
IAU|56.72|63.29|4936.62|4.64|4.64
CASH|||22.31||
'''),
 'glif_am_04':dict(page=36,as_of=None,period_raw='보고서 p36 현황; 그래프 눈금 19-Sep~28-Nov, 표 기준일 명시 없음',rows='''
SMH|305.25|359.43|6469.74|17.75|5.97
IGV|110.52|105.49|17194.87|-4.55|0
XOVR|20.81|19.77|4883.19|-4.99|4.51
EWJV|38.98|40.19|5827.55|3.10|5.38
TSLA|347.8|442.23|3095.61|27.15|0
APP|582|580.7|2322.80|-0.22|0
PLTR|170.52|170.69|7339.67|0.10|6.78
NVDA|170.75|181.46|5443.80|6.27|5.03
RDDT|198.55|193.31|1739.79|-2.64|0
PANW|202.08|218.26|1964.34|8.01|0
RBLX|126.43|102.28|306.84|-19.10|0
IBM|291.54|301.78|4526.70|3.51|4.18
XLE|85.46|90.14|3876.02|5.48|3.58
WM|208.67|214.54|4290.80|2.82|3.96
GOOG|275.44|316.02|9796.62|14.73|9.05
PM|153.35|153.35|4174.74|0.83|3.85
JNJ|199.58|205.42|4313.82|2.93|3.98
SHV|110.28|110.14|4405.60|-0.13|4.07
TLT|89.46|88.81|6216.70|-0.72|5.74
IAU|68.53|79.29|4202.37|15.70|3.88
CASH|||32540.67||30.04
'''),
 'glif_am_06':dict(page=44,as_of='2026-06-03',period_raw='Jun 3 (p44 footnote; year from 26-1 report)',rows='''
MU|621.45|1063.92|23406|71.2|4.2
MRVL|190.69|290.80|45656|52.5|8.2
005930.KS|158.27|236.30|62147|49.3|11.1
SNDK|1326.76|1716.82|34336|29.4|6.1
CSCO|115.53|128.01|55300|10.8|9.9
LLY|963.33|1064.48|57482|10.5|10.3
KMI|32.34|31.43|24358|-2.8|4.3
COST|1050.45|953.81|44829|-9.2|8.0
VRTX*|472.20|492.38|0|4.3|0.0
HII*|425.26|413.70|0|-2.7|0.0
CRS*|429.41|408.93|0|-4.8|0.0
034020.KS*|86.54|70.19|0|-18.9|0.0
TLT*|85.83|85.83|0|0.0|0.0
CPER|36.23|40.61|19574|12.1|3.5
USO|142.83|137.26|16608|-3.9|3.0
SHV*|110.30|110.12|0|-0.2|0.0
CASH|||175878||31.4
''')}

def C(s,p,period,entries,reason,event,exact=None,flags=None):
    for ticker,action,delta in entries:
        CHANGES.append(dict(source_id=f'glif_am_{s:02}',source_pages=[p],period_raw=period,
            reported_ticker=ticker,action=action,weight_change_pp=delta,rationale=reason,
            market_event=event,event_date=exact,quality_flags=flags or []))
C(2,46,'Feb 6, 2025',[('SMH','reduce',-6.04),('IGV','reduce',-5.97),('SHV','initiate',12.36),('TLT','initiate',2.40)],'금리·지정학 위험을 낮추기 위해 주식 일부를 채권으로 이동','DeepSeek, 관세 발언, 미중 갈등','2025-02-06')
C(2,51,'Early Mar / first week of March 2025',[('IBB','exit',-3.88),('NVDA','initiate',3.88)],'금리 민감 바이오 ETF를 청산하고 이익 성장 대비 평가 매력이 있다는 NVDA로 전환','연준의 신중한 금리 결정과 정책 불확실성')
C(2,63,'Late May 2025',[('SHV','reduce',-1.04),('TLT','increase',1.64),('IGV','increase',0.30)],'장기 국채의 가격 매력을 판단해 듀레이션과 소프트웨어 비중 확대','Moody’s 신용등급 하향, EU 관세 우려')
C(4,59,'Mid Oct 2025',[('RDDT','reduce',None),('RBLX','reduce',None),('XLE','increase',None),('TLT','increase',None)],'급등 성장주 이익 실현과 에너지·국채 방어자산 보강','기술주 평가 부담과 지정학적 위험',flags=['ocr_weight_changes_not_verified_not_extracted'])
C(4,63,'Mid Nov 2025',[('APP','exit',None),('RDDT','exit',None),('RBLX','exit',None),('GOOG','increase',None),('PM','increase',None),('JNJ','increase',None),('WM','increase',None)],'투기적 AI 노출을 낮추고 현금흐름이 견조한 자산으로 전환','AI 평가 부담과 연준 인하 기대 변화',flags=['ocr_weight_changes_not_verified_not_extracted'])
C(6,72,'Early May 2026',[('SHV','exit',-36.5),('LLY','initiate',10.0),('005930.KS','initiate',9.6),('CRS','initiate',7.2),('MU','initiate',6.7),('SNDK','initiate',6.6),('034020.KS','initiate',6.6),('KMI','initiate',4.8),('CPER','initiate',3.4),('USO','initiate',3.3)],'기업 실적과 CAPEX 가이던스 확인 후 현금성 자산에서 위험자산으로 재배분','메모리 실적 개선, 에너지 공급 위험')
C(6,74,'Mid May 2026',[('005930.KS','reduce',-1.9),('MU','reduce',-1.9),('SNDK','reduce',-1.8),('CSCO','initiate',9.7)],'같은 메모리 사이클에 노출된 종목의 이익을 실현하고 CSCO 편입','메모리 묶음 비중 약44%, Cisco 실적 발표')
C(6,76,'Late May 2026',[('CRS','exit',-6.8),('034020.KS','exit',-5.3),('MU','reduce',-3.1),('COST','initiate',9.5),('MRVL','initiate',5.7)],'손절 규칙에 따라 청산하고 AI 네트워크·필수소비재로 전환','원자재 변동성과 WMT 실적 부진',flags=['source_net_realized_pnl_arithmetic_conflict'])

def N(sid,pages,entities,industries,summary,thesis,catalysts,risks,relations=None,flags=None):
    NOTES.append(dict(source_id=sid,source_pages=pages,related_entities=entities,related_industries=industries,
        summary=summary,investment_thesis=thesis,growth_catalysts=catalysts,risk_factors=risks,
        relationships=relations or [],quality_flags=flags or []))
def R(a,b,typ):return {'subject':a,'object':b,'relation':typ,'attribution':'report_assertion_not_independently_verified'}
N('glif_im_11',[4,34,36,38],['GS','S-OIL','SK이노베이션'],['정유'],
 '정제마진과 제품 전환을 중심으로 정유사의 이익 구조를 분석한다.',
 ['공급 회복 지연이 정제마진을 지지한다는 판단','투자 완료와 신규 공정의 현금흐름 개선 기대'],
 ['샤힌 가동','SAF·액침냉각유 확대'],[],[R('GS','GS칼텍스','indirect_ownership')])
N('glif_im_10',[32,33,34,35],['신성이엔지','SK엔무브','LG전자','Vertiv'],['산업용 냉각시스템'],
 '데이터센터의 고밀도화가 냉각설비와 유체 공급망 수요로 연결된다는 분석이다.',
 ['냉각 장비·설치·운영을 함께 공급하는 역량의 가치'],['AI 서버 증설','통합 냉각솔루션 실증'],
 ['AI 설비투자 둔화','액침냉각 매출 비중이 별도 공개되지 않음'],[R('SK엔무브','LG전자','cooling_solution_collaboration'),R('SK엔무브','GRC','cooling_solution_collaboration')],['some_pdf_headings_have_font_mapping_corruption'])
N('glif_im_09',[31,33,35],['삼성중공업','한화오션','대한조선'],['조선'],
 'FLNG, 특수선, 탱커 등 회사별 강점과 수주 경로를 구분한다.',
 ['고부가 선종의 진입장벽','수출과 MRO 사업 확대'],['에너지 안보 수요','노후선 교체'],[],
 [R('한화오션','한화에어로스페이스','propulsion_weapons_group_collaboration'),R('한화오션','한화시스템','sensors_communications_group_collaboration')],['report_hanwha_ocean_ticker_242660_is_inconsistent_with_KRX_042660'])
N('glif_im_08',[38,39],['HD현대일렉트릭','일진전기'],['전력인프라'],
 '수주·증설과 북미 전력기기 수요를 연결해 매출 가시성을 논한다.',
 ['수익성 높은 제품과 지역 비중 확대','상위 전압망 확장이 하위 설비 수요로 연결'],['공장 증설','초고압 전력망 투자'],[])
N('glif_im_07',[35,36],['삼성바이오로직스','한미약품'],['제약·바이오'],
 '생산능력 확장과 신약 임상·상업화 일정을 성장 요인으로 제시한다.',
 ['CDMO 규모와 고객 기반','비만·대사질환 파이프라인 성과 기대'],['신규 생산시설','임상 결과와 상업화'],[],
 [R('한미약품','MSD','mash_pipeline_partnership')],['cover_2025_02_06_body_2026_02_06_listing_2026_01_31_conflict'])
N('glif_im_06',[28,31],['Rocket Lab','인텔리안테크'],['위성'],
 '발사체·위성 시스템 통합과 지상 안테나 수요를 서로 다른 투자 경로로 제시한다.',
 ['저궤도 위성망 확대에 따른 지상 인프라 수요','수직계열화의 고객 편의'],['Neutron 개발','게이트웨이 수주'],[],
 [R('Rocket Lab','SpaceX','launch_competition'),R('인텔리안테크','OneWeb','antenna_supply_collaboration')])
N('glif_im_05',[29,31,33],['한화에어로스페이스','풍산','LIG넥스원'],['방산'],
 '현지 거점 투자와 탄약·유도무기 수출 확대를 분석한다.',
 ['해외 수주와 현지화로 중기 성장 확보','첨단 무인체계 기술 투자'],['해외 합작법인','탄약 생산능력 확대'],[],
 [R('한화에어로스페이스','GA-ASI','unmanned_aircraft_joint_development')],['some_segment_shares_and_backlog_period_require_review'])
N('glif_im_04',[30,31],['에이피알','코스맥스'],['화장품'],
 '브랜드·뷰티기기 해외 확장과 ODM의 생산 역량을 구분해 평가한다.',
 ['현지 마케팅에서 오프라인 유통으로의 확장','제품 개발 역량 기반 ODM 경쟁력'],['유럽 채널 확대','신흥시장 고객 확보'],[],
 [R('에이피알','실리콘투','distribution_channel')],['APR_market_label_conflict_current_KRX_is_KOSPI'])
N('glif_im_03',[28,29,30,31],['SK하이닉스','삼성전자','한미반도체','ISC'],['HBM'],
 'HBM 경쟁력과 장비·테스트 부품의 수요 확대를 회사별로 구분한다.',
 ['HBM 제품 믹스와 고객 확대','해외 고객 설비투자에 따른 장비 수요'],['HBM4 전환','ASIC·CPU 테스트 수요'],
 ['TC본더 경쟁 심화','하이브리드 본딩 도입에 따른 기술 변화'],[R('SK하이닉스','NVIDIA','hbm_supplier'),R('한미반도체','HBM 고객사','equipment_supplier')])
N('glif_im_02',[27,28,29,30,33],['비에이치아이','두산에너빌리티','한국수력원자력'],['원자력'],
 '원전 수출의 금융·정책 지원과 기자재 공급망을 분석한다.',
 ['기술과 시공 역량의 국제 협력','기자재와 정비의 반복 수요'],['SMR 개발','해외 원전 사업'],
 ['정책 불확실성','부지·안전성·주민 수용성'],[R('비에이치아이','두산에너빌리티','equipment_supply_network')],['BHI_financial_period_missing'])
N('glif_im_01',[63,64,65,66],['FANUC','Leader Drive','Tesla'],['로봇'],
 '자동화·정밀부품·휴머노이드의 성장 경로와 분산 투자 논리를 검토한다.',
 ['자동화 가치사슬 통합','휴머노이드 핵심 부품 수요 기대'],['스마트팩토리','휴머노이드 양산 계획'],
 ['기술 흐름 미확정','Tesla 유럽 수요와 정치적 논란'],[],['p65_company_and_currency_mixed_block_not_extracted','unidentified_ETF_constituents_not_treated_as_GLIF_holdings'])
N('glif_am_01',[5,6,11,12,13,33,34],['미국','AI 주식','국채'],['거시·자산배분'],
 '고용의 양과 질, 관세 물가 압력, AI 생산성을 함께 평가한다.',
 ['실적 안정성이 있는 AI 기업 선별','금리 환경에 맞춘 채권 운용'],['생산성 투자'],
 ['고평가 성장주의 금리 민감도','Fed Put 효과 약화'])
N('glif_am_02',[13,16,21,32,46,51,63],['GLIF GAA 25-1'],['거시·자산배분'],
 '주식·헤지자산 배분과 과거 리밸런싱을 설명한다.',
 ['채권으로 방어력을 보강','바이오에서 NVDA로 전환한 상대가치 판단'],['기업 이익 성장'],
 ['관세 불확실성','금리 민감도'],[],['reported_holding_returns_and_inflation_tables_have_conflicts','retrospective_rebalancing'])
N('glif_am_03',[11,17,20,35,36],['미국','국채'],['거시·자산배분'],
 '고용 위험에 대응한 금리 인하와 장기 금리의 하방 경직성을 함께 논한다.',
 ['선별적 주식 투자','듀레이션 위험 관리'],['생산성 개선'],['재정 위험','소비·생산 단계 물가 괴리'])
N('glif_am_04',[35,36,37,59,63,65,66],['GLIF GAA 25-2','GOOG','PM','JNJ','WM'],['거시·자산배분'],
 '성장주 평가 부담에 대응해 우량 성장주와 방어자산을 함께 보유하는 구상을 제시한다.',
 ['현금흐름과 가격 전가력 선호','에너지·금으로 위험 분산'],['기업별 이익 가시성'],['고금리','재정 위험','AI 평가 부담'],[],
 ['ocr_selected_pages_reviewed','zero_weight_positive_market_value_conflicts','retrospective_rebalancing'])
N('glif_am_05',[19,20,22,42,43],['미국','AI 인프라'],['거시·자산배분'],
 '고용 약화와 에너지 충격, 생산성 개선의 상충 관계를 해석한다.',
 ['헤드라인 지표와 노동시장 내부 구조를 함께 검토'],['AI 생산성 투자'],
 ['에너지발 인플레이션','고금리와 재정 부담'],[],['headline_CPI_conflicts_with_same_report_table'])
N('glif_am_06',[44,45,46,72,74,76,77,80,81],['GLIF GAA 26-1','MU','MRVL','CSCO','COST'],['거시·자산배분'],
 '현금 보유 후 재진입, 메모리 집중도 완화, 손절 후 종목 전환을 사후 설명한다.',
 ['실적 확인 후 재배분','상관관계가 높은 종목군의 집중도 관리'],['기업 실적 확인'],
 ['현금 보유의 기회비용','IT 집중도','에너지 위험'],[],['retrospective_not_contemporaneous','benchmark_label_conflict_SP500_vs_Nasdaq','realized_pnl_arithmetic_conflict'])
N('glif_am_07',[9,12,20,30],['미국','회사채','국채'],['거시·자산배분'],
 '신용등급별 조달 비용 차이와 개정 GDP, 일부 기간만 포함하는 물가 평균을 구분한다.',
 ['평균 금융여건보다 취약 차주의 신용 접근성 확인'],[],
 ['저신용 스프레드 확대','높은 주택 신용 가격','지표 수정과 부분 분기 비교'],[],['Q3_inflation_average_contains_only_July_August'])
