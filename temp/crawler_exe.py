import os
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool
import concurrent.futures
import pandas as pd
from tqdm import tqdm
import time
import argparse


def do_crawling(row: object) -> None:
    """
    crawling 파라미터를 받고 category_big.py를 실행시키는 함수
    :param row: dataframe iterrows
    :return: None
    """
    os.system(
        f"python crawler/category_big.py "
        + f"-mg {row[1].mgmt_lv} "
        + f"-s {row[1].start_dt} -e {row[1].end_dt} "
        + f"-d {row[1].device} -g {row[1].gender} -a {row[1].age}"
    )


def do_process_with_thread_crawl(row: object) -> None:
    """
    do_thread_crawl함수를 실해시키기 위한 함수
    :param row: dataframe iterrows
    :return: None
    """
    do_thread_crawl(row)


def do_thread_crawl(row: object) -> None:
    """
    멀티쓰레드를 부여
    :param row: dataframe iterrows
    :return: None
    """
    thread_list = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        thread_list.append(executor.submit(do_crawling, row))
        for execution in concurrent.futures.as_completed(thread_list):
            execution.result()


if __name__ == "__main__":

    __file__ = "./temp/crawler_exe.py"

    parser = argparse.ArgumentParser(description="Command-line에서 카테고리레벨")

    parser.add_argument("--mgmt_lv", "-mg",
                        required=True,
                        help="mgmt_lv - 카테고리 대 or 중")

    args = parser.parse_args()

    start_dt = pd.DataFrame(
        [d.strftime("%Y%m%d") for d in pd.date_range("20220101", "20220101")],
        columns=["start_dt"],
    )
    end_dt = pd.DataFrame(
        [d.strftime("%Y%m%d") for d in pd.date_range("20220101", "20220101")],
        columns=["end_dt"],
    )

    device = pd.DataFrame(["1_2"], columns=["device"])
    gender = pd.DataFrame(["1"], columns=["gender"])
    age = pd.DataFrame(["1"], columns=["age"])

    df = pd.concat([start_dt, end_dt], axis=1)
    df = pd.merge(
        df,
        pd.merge(device, pd.merge(gender, age, how="cross"), how="cross"),
        how="cross",
    )

    df["mgmt_lv"] = args.mgmt_lv
    start_time = time.time()

    total = len(df)
    pool = Pool(3)

    with tqdm(total=total) as pbar:
        for _ in tqdm(pool.map(do_process_with_thread_crawl, df.iterrows())):
            pbar.update()

    print(f"총소요 시간: {time.time() - start_time}")
