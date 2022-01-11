import pandas as pd

data1 = pd.read_excel('./src/category_lv3.xlsx')
data2 = pd.read_csv('./src/naver_goods_cat.csv')

temp1 = data1[['category_1', 'category_1nm']].drop_duplicates('category_1', keep='first')
temp2 = data2[['category_1', 'category_1nm_x']].drop_duplicates('category_1', keep='first')

pd.merge(temp1, temp2, on='category_1', how='outer')


from functools import reduce

age = "10-20"

age_list = [0, 0, 0, 0, 0, 0, 0]
for i in list(age.split('-')):
    age_list[int(i) // 10] += 1


import psycopg2
import pandas as pd


host = 'postgres-aivelabs.cu41dqju3sxw.ap-northeast-2.rds.amazonaws.com'
dbname = 'postgres'
user = 'postgres'
password = 'aivelabs1004!'
port = 5432

db=psycopg2.connect(host=host,
                          dbname=dbname,
                          user=user,
                          password=password,
                          port=port)
cur = db.cursor()


with open('./data/category_lv1_result_20220106+20210101+20210101+1_2+1_2+1_2.csv', 'r', encoding='utf-8') as f:
    #f , <database name>, Comma-Seperated
    cur.copy_from(f, 'crawling_mart.nv_kw_ctgr_lv1', sep=',')
    #Commit Changes
    db.commit()
    #Close connection
    db.close()


f.close()
