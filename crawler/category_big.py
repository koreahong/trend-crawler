from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool
import time
import pandas as pd
from tqdm import tqdm
import argparse
import datetime
import collections
import warnings
warnings.filterwarnings("ignore")


def set_chrome_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(
        "User-Agent=Mozilla/5.0 (Windows NT 6.3; Win64; x64) "
        + "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    )

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver


year_dict = collections.defaultdict(int)
for idx, year in enumerate(range(2017, 2030), start=1):
    year_dict[str(year)] = idx

# 금일 출력
today_dt = datetime.datetime.now()
today_dt = today_dt.strftime("%Y%m%d")


parser = argparse.ArgumentParser(description="Command-line에서 디바이스, 성별, 연령, 날짜 반환")

parser.add_argument(
    "--start_dt",
    "-s",
    required=True,
    help="검색기간 - 시작일자 ex) 20211208"
)

parser.add_argument(
    "--end_dt",
    "-e",
    required=True,
    help="검색기간 - 종료일자 ex) 20211208"
)

parser.add_argument(
    "--device",
    "-d",
    required=True,
    help="탐색기기 입력(ex 1_2: 1:모바일 2:pc), 형식 : str",
)

parser.add_argument(
    "--gender",
    "-g",
    required=True,
    help="탐색성별 입력(ex 1_2: 1:여성 2:남성), 형식 : str",
)

parser.add_argument(
    "--age",
    "-a",
    required=True,
    help="탐색연령대 입력,(ex 1_2: 10대 & 20대), 형식 : str",
)

args = parser.parse_args()

start_dt = args.start_dt
end_dt = args.end_dt
device = args.device
age = args.age
gender = args.gender

print("시작일 : ", start_dt, " / 종료일 : ",  end_dt, " ------ 시작")

# 연령대 파라미터가 10_20일 경우 [0,1,1,0,0,0,0]으로 변환
for var_name in ['device_lst', 'gender_lst', 'age_lst']:
    globals()[f'{var_name}'] = [0, 0, 0, 0, 0, 0, 0]
    for search_detail_idx in list(globals()[f'{var_name[:-4]}'].split('_')):
        globals()[f'{var_name}'][int(search_detail_idx) % 10] += 1


cate_list = pd.read_excel("./src/crawler_base/category_lv3.xlsx")
category_lv2 = cate_list[['category_1', 'category_1nm', 'lv1_num']].drop_duplicates('category_1', keep='first')

keyword_df = pd.DataFrame()

driver = set_chrome_driver()
url = "https://datalab.naver.com/shoppingInsight/sCategory.naver"
driver.get(url)

DOING = True

try:
    element = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.CLASS_NAME, "insite_form"))
    )
except:
    driver.quit()

# 기기체크
for idx, bool_ in enumerate(device_lst):
    if bool_ == 1:
        driver.find_element_by_xpath('//*[@id="18_device_'
                                     + str(idx)
                                     + '"]').click()

# 성별체크
for idx, bool_ in enumerate(gender_lst):
    if bool_ == 1:
        driver.find_element_by_xpath('//*[@id="19_gender_'
                                     + str(idx)
                                     + '"]').click()

# 연령체크
for idx, bool_ in enumerate(age_lst):
    if bool_ == 1:
        driver.find_element_by_xpath('//*[@id="20_age_'
                                     + str(idx)
                                     + '"]').click()




# 시작, 끝 년도 위치 잡기
# 시작기준 2017 -> 1, 2022 -> 6
# start_year_xpath_num = (int(datetime.datetime.now().year) - 2017 + 1) + (int(start_dt[:4]) - int(datetime.datetime.now().year))
# end_year_xpath_num = int(datetime.datetime.now().year) - int(start_dt[:4])

error_list = []
try:
    # 1: 시작기간, 3: 종료시간
    start_order = 1
    end_order = 3

    # order1 - 검색시작 연도를 끝시작 연도에 맞춘다
    # 연 - 체크박스 클릭
    driver.find_element_by_xpath(
        '//*[@id="content"]/div[2]/div/div[1]/div/div/div[2]/div[2]/span['
        + str(start_order)
        + ']/div[1]/span'
    ).click()

    # 연 - 세부사항 클릭
    driver.find_element_by_xpath(
        '//*[@id="content"]/div[2]/div/div[1]/div/div/div[2]/div[2]/span['
        + str(start_order)
        + ']/div[1]/ul/li['
        + str(year_dict[end_dt[:4]])
        + ']/a'
    ).click()
    # time.sleep(0.5)


    # 월 - 체크박스 클릭
    driver.find_element_by_xpath(
        '//*[@id="content"]/div[2]/div/div[1]/div/div/div[2]/div[2]/span['
        + str(start_order)
        + ']/div[2]/span'
    ).click()
    # time.sleep(0.5)

    # 월 - 세부사항 클릭
    driver.find_element_by_xpath(
        '//*[@id="content"]/div[2]/div/div[1]/div/div/div[2]/div[2]/span['
        + str(start_order)
        + ']/div[2]/ul/li['
        + str(1)
        + "]/a"
    ).click()
    # time.sleep(0.5)

    # 일 - 체크박스 클릭
    driver.find_element_by_xpath(
        '//*[@id="content"]/div[2]/div/div[1]/div/div/div[2]/div[2]/span['
        + str(start_order)
        + ']/div[3]/span'
    ).click()
    # time.sleep(0.5)

    # 일 - 세부사항 클릭
    driver.find_element_by_xpath(
        '//*[@id="content"]/div[2]/div/div[1]/div/div/div[2]/div[2]/span['
        + str(start_order)
        + ']/div[3]/ul/li['
        + str(1)
        + "]/a"
    ).click()

    # order2 - 끝시간 맞추기
    # 연 - 체크박스 클릭
    driver.find_element_by_xpath(
        '//*[@id="content"]/div[2]/div/div[1]/div/div/div[2]/div[2]/span['
        + str(end_order)
        + ']/div[1]/span'
    ).click()

    # 연 - 세부사항 클릭
    driver.find_element_by_xpath(
        '//*[@id="content"]/div[2]/div/div[1]/div/div/div[2]/div[2]/span['
        + str(end_order)
        + ']/div[1]/ul/li/a'
    ).click()
    # time.sleep(0.5)

    # 월 - 체크박스 클릭
    driver.find_element_by_xpath(
        '//*[@id="content"]/div[2]/div/div[1]/div/div/div[2]/div[2]/span['
        + str(end_order)
        + ']/div[2]/span'
    ).click()
    # time.sleep(0.5)

    # 월 - 세부사항 클릭
    driver.find_element_by_xpath(
        '//*[@id="content"]/div[2]/div/div[1]/div/div/div[2]/div[2]/span['
        + str(end_order)
        + ']/div[2]/ul/li['
        + str(int(end_dt[4:6]))
        + "]/a"
    ).click()
    # time.sleep(0.5)

    # 일 - 체크박스 클릭
    driver.find_element_by_xpath(
        '//*[@id="content"]/div[2]/div/div[1]/div/div/div[2]/div[2]/span['
        + str(end_order)
        + ']/div[3]/span'
    ).click()
    # time.sleep(0.5)

    # 일 - 세부사항 클릭
    driver.find_element_by_xpath(
        '//*[@id="content"]/div[2]/div/div[1]/div/div/div[2]/div[2]/span['
        + str(end_order)
        + ']/div[3]/ul/li['
        + str(int(end_dt[6:]))
        + "]/a"
    ).click()

    # order3 - 시작시간 맞추기
    if end_dt[:4] == '2017':
        pass
    else:
        # 연 - 체크박스 클릭
        driver.find_element_by_xpath(
            '//*[@id="content"]/div[2]/div/div[1]/div/div/div[2]/div[2]/span['
            + str(start_order)
            + ']/div[1]/span'
        ).click()

        # 연 - 세부사항 클릭
        driver.find_element_by_xpath(
            '//*[@id="content"]/div[2]/div/div[1]/div/div/div[2]/div[2]/span['
            + str(start_order)
            + ']/div[1]/ul/li['
            + str(year_dict[start_dt[:4]])
            + "]/a"
        ).click()
        # time.sleep(0.5)

    if end_dt[4:6] == '01':
        pass
    else:
        # 월 - 체크박스 클릭
        driver.find_element_by_xpath(
            '//*[@id="content"]/div[2]/div/div[1]/div/div/div[2]/div[2]/span['
            + str(start_order)
            + ']/div[2]/span'
        ).click()
        # time.sleep(0.5)

        # 월 - 세부사항 클릭
        driver.find_element_by_xpath(
            '//*[@id="content"]/div[2]/div/div[1]/div/div/div[2]/div[2]/span['
            + str(start_order)
            + ']/div[2]/ul/li['
            + str(int(start_dt[4:6]))
            + "]/a"
        ).click()

    if end_dt[6:] == '01':
        pass
    else:
        # 일 - 체크박스 클릭
        driver.find_element_by_xpath(
            '//*[@id="content"]/div[2]/div/div[1]/div/div/div[2]/div[2]/span['
            + str(start_order)
            + ']/div[3]/span'
        ).click()
        # time.sleep(0.5)

        # 일 - 세부사항 클릭
        driver.find_element_by_xpath(
            '//*[@id="content"]/div[2]/div/div[1]/div/div/div[2]/div[2]/span['
            + str(start_order)
            + ']/div[3]/ul/li['
            + str(int(start_dt[6:]))
            + "]/a"
        ).click()
        # end_dt 설정 -------------------------


    for j, cat2_row in category_lv2.iterrows():
        time.sleep(0.5)
        lv1_num = cat2_row["lv1_num"]

        # 카테고리 설정
        driver.find_element_by_xpath(
            '//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[1]/span'
        ).click()  # 버튼 클릭 후 1차 카테고리
        time.sleep(0.2)
        driver.find_element_by_xpath(
            '//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[1]/ul/li['
            + str(lv1_num)
            + "]/a"
        ).click()  # 세부카테고리 선택
        time.sleep(0.2)

        # 조회하기 클릭
        driver.find_element_by_xpath('//*[@id="content"]/div[2]/div/div[1]/div/a').click()

        # 1차 카테고리->2차 카테고리의 키워드 순위 조회
        # 키워드 순위 총 500개가 페이지별로 20위씩까지 조회가능
        # 1~100위까지 수집 계획
        time.sleep(0.5)
        keyword_list = []  # 1~100위까지 키워드 넣을 리스트
        # p = 수집할 페이지 수, 테스트를 위해선 1을 수정
        for p in range(0, 5):
            time.sleep(0.5)
            # 인기검색어 가져오기
            should_restart = True
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            keyword_rank_content = soup.select(
                "#content > div.section_instie_area.space_top > div > div:nth-of-type(2) > div.section_insite_sub > div > div > div.rank_top1000_scroll > ul > li"
            )
            # print("페이지 내 키워드 수 :", len(keyword_rank_content), p + 1, "페이지")
            time.sleep(0.3)
            if len(keyword_rank_content) == 20:
                while should_restart:  # 각 페이지 수집을 위한 안전장치
                    page_list = (
                        []
                    )  # 페이지별로 보기, 즉 키워드 20개씩 넣을 리스트; 각 페이지는 20위씩 있음-> 5페이지 조회하면 1~100위까지 볼 수 있어서 위에 range(0,5)로 for loop
                    for i in range(1, 21):  # 1~20,21~40,...,81~100
                        # should_restart =True
                        # while should_restart:
                        keyword_path = f'//*[@id="content"]/div[2]/div/div[2]/div[2]/div/div/div[1]/ul/li[{i}]/a'
                        # page_list=[]
                        if (
                                int(
                                    driver.find_element_by_xpath(keyword_path).text.split("\n")[
                                        0
                                    ]
                                )
                                > 100
                        ):  # 100위를 넘어서 101위,102위 ...수집하게 되면 다음 카테고리에서 앞 순위들이 누락됨-> 100위 넘기면 더이상 수집못하게 조건문 걸어놓음
                            should_restart = False  # while문 탈출
                            break
                        else:
                            page_list.append(
                                driver.find_element_by_xpath(keyword_path).text
                            )
                    # 인기검색어 순위가 20개가 되지 않을때 예외처리도 진행해야함
                    if len(page_list) == 20 or (
                            driver.find_element_by_xpath(
                                f'//*[@id="content"]/div[2]/div/div[2]/div[2]/div/div/div[2]/span/em'
                            ).text
                            == "6"
                            and int(
                        driver.find_element_by_xpath(keyword_path).text.split("\n")[0]
                    )
                            > 100
                    ):
                        # 페이지에서 수집한 상품이 20개가 되었을때, 혹은 페이지 넘버가 6이면서 상품순위는 100위가 넘었을때 수집 멈추게끔
                        should_restart = False  # while문 탈출
                        time.sleep(0.2)
                        for page_keyword in page_list:
                            keyword_list.append(
                                page_keyword
                            )  # 키워드 리스트에 20개씩 5번 넣어줌->1~100위 리스트 생성
                driver.find_element_by_xpath(
                    '//*[@id="content"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/a[2]'
                ).click()
                time.sleep(0.2)
            else:
                print("검색어 갯수가 20 미만입니다\n")
                break

        # 카테고리 값 추출
        category = driver.find_element_by_xpath(
            '//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[1]/span'
        ).text

        category_1nm = category_lv2[category_lv2["category_1nm"] == category].iloc[0][
            "category_1nm"
        ]

        df = pd.DataFrame()
        df = pd.DataFrame(
            list(map((lambda x: x.split("\n")), keyword_list)), columns=["순위", "인기검색어"]
        )

        # time.sleep(0.3)

        df["category_1nm"] = category_1nm
        df["category_1"] = cat2_row.category_1
        # time.sleep(0.3)

        keyword_df = keyword_df.append(df)
        print("시작일 : ", start_dt, " / 종료일 : ",  end_dt, " --- ", category_1nm, " ------ 완료\n")
        time.sleep(2)
    # 수집 완료 후 데이터 프레임 생성
    today_dt = datetime.datetime.now()
    today_dt = today_dt.strftime("%Y%m%d")

    # 데이터 조인
    # 현재는 카테고리 lv2로 되어있으나 추후 카테고리 갱신시 코드 상위 카테고리 변수 정정
    new = pd.merge(left=keyword_df, right=category_lv2, how="left")

    # 컬럼 이름 변경
    new.rename(
        columns={
            "인기검색어": "keyword_nm",
            "순위": "keyword_rk",
            "category_1": "ctgr_lclas_id",
            "category_1nm": "ctgr_lcalas_nm",
            "lv1_num": "lv1_num",
        },
        inplace=True,
    )

    new['start_dt'] = start_dt
    new['end_dt'] = end_dt
    new['register_dt'] = today_dt
    new['device'] = device
    new['age'] = age
    new['gender'] = gender

    new.to_csv(
        f"./data/category_lv1_result_{today_dt}+{start_dt}+{end_dt}+{device}+{gender}+{age}.csv",
        encoding="utf-8-sig",
        index=False,
    )
    print(f"./data/category_lv1_result_{today_dt}+{start_dt}+{end_dt}+{device}+{gender}+{age}.csv 저장완료\n")

    # 기존 CSV 내보내기
    keyword_df.to_csv(
        f"./data/keyword_top100_{today_dt}+{start_dt}+{end_dt}+{device}+{gender}+{age}.csv",
        index=False,
        encoding="utf-8-sig",
    )
    print(today_dt, ' / ', start_dt, "전처리 데이터 가공 및 csv 추출완료")
    script_end = time.time()
    print("시작일 : ", start_dt, " / 종료일 : ", end_dt , " ------ 종료\n")

except:
    print("시작일 : ", start_dt, " / 종료일 : ", end_dt, " ------ 오류\n")

finally:
    driver.quit()