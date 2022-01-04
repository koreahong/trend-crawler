import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import engine
import psycopg2
import pandas as pd
import datetime
from pathlib import Path
from sqlalchemy import create_engine
import time
from datetime import datetime ,  timedelta

#카테고리 엑셀 로드 > 마지막 카테고리 이름 추출
catexcel = pd.read_excel('/var/lib/airflow/workspace/tony/src/category_lv3.xlsx')
last_cat = catexcel['category_1nm']
last_cat = last_cat.iloc[-1]
last_cat

#금일 날짜 계산()
strt =datetime.today() - timedelta(8)
strt = strt.strftime("%Y%m%d")
yesterday = datetime.today() - timedelta(1)
yesterday = yesterday.strftime("%Y%m%d")
#파일 호출
home_path = str(Path(__file__).absolute().parent)
src_path = home_path + "/result"
col_names = ['keyword_rank','keyword_nm','ctgr_mclas_id','ctgr_mclas_nm','register_dt','gender','age','collect_dt','ctgr_lclas_id','ctgr_lcalas_nm']
#df = pd.read_csv('/var/lib/airflow/workspace/tony/result/result_2021-12-22_2_2.csv')
df = pd.read_csv(src_path +'/result_2021-12-16_1_1.csv', names = col_names, header=None)

#df = pd.read_csv('/var/lib/airflow/workspace/tony/result/keyword_top100_{startdate}_{enddate}_{last_cat}.csv'.format(startdate = strt, enddate = yesterday, last_cat = last_cat))

#1. 키워드 데이터 csv 데이터프레임 > DB로 적재하기
#df['create_date'] = datetime.today().strftime("%Y%m%d")

# Insert
#conn = sqlite3.connect("postgresql://postgres:aivelabs1004!@postgres-aivelabs.cu41dqju3sxw.ap-northeast-2.rds.amazonaws.com:5432/postgres")
engine = create_engine("postgresql://postgres:aivelabs1004!@postgres-aivelabs.cu41dqju3sxw.ap-northeast-2.rds.amazonaws.com:5432/postgres")
df.to_sql(name="naver_keyword", schema="crawling_mart", con=engine, if_exists = 'append', index=False)



#2. 상품100개 데이터 csv 데이터프레임 > DB로 적재하기
#df_goods > test_goods에서 크롤링한 결과물 csv로 내보내기
#df_goods.read_csv('/var/lib/airflow/workspace/tony/result/naver_best100_{date}.csv')
#df_goods.to_sql(name="crawl_sample", schema="crawling_mart", con=engine, if_exists = 'append', index=False)
