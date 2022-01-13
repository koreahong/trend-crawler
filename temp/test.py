import psycopg2
import glob
from tqdm import tqdm
import pandas as pd
import re
from multiprocessing import Pool
from typing import Sequence


def do_db_insert(files: Sequence[str]) -> None:
    for file in tqdm(files):

        data = pd.read_csv(file)
        sql = f'''INSERT INTO crawling_mart.nv_kw_ctgr_lv1 {tuple(data.columns.to_list())}
                VALUES '''.replace("'", '')
        for idx, row in enumerate(data.itertuples(index=False)):
            if len(row) == len(data.columns.to_list()):
                data_preprocessing = pd.Series(row).apply(lambda x: re.sub("[',]", '', str(x)))
                data_preprocessing = data_preprocessing.apply(lambda x: re.sub('["]', '', str(x)))
                sql += f'''{tuple(data_preprocessing.transpose().values)},'''
            else:
                error_list.append(file + str(idx))
        sql = sql[:-1]
        cur.execute(sql)
        db.commit()

    db.close()
    print('csv to db 완료')


if __name__ == '__main__':
    host = 'postgres-aivelabs.cu41dqju3sxw.ap-northeast-2.rds.amazonaws.com'
    dbname = 'postgres'
    user = 'postgres'
    password = 'aivelabs1004!'
    port = 5432

    db = psycopg2.connect(host=host,
                          dbname=dbname,
                          user=user,
                          password=password,
                          port=port)
    cur = db.cursor()

    csv_files = glob.glob('./data/category*.csv')

    error_list = []

    total = len(csv_files)
    pool = Pool(5)
    with tqdm(total=total) as pbar:
        for _ in tqdm(pool.map(do_db_insert, csv_files)):
            pbar.update()
