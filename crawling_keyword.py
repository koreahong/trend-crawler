from datetime import timedelta
from os import path
from pyvirtualdisplay import Display
from pathlib import Path
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import json
import requests
from urllib.request import Request, urlopen
from selenium import webdriver
import time
import pandas as pd
import openpyxl
from tqdm import tqdm
import argparse
import datetime

"""
-- sn: 순번 // sequence <- 포스트그레스 시퀀스 
	-- register_dt: 등록일자 date / 2021-12-14 / date
	-- 성별: M/F(1,2)
	-- 연령대 (10대, 20~30대, 40~60대) <- (1, 2, 3)
	-- keyword_nm 키워드 : varchar(50)
	-- keyword_rank 키워드_순위: intger
	-- ctgr_lclas_id 카테고리_대분류_id varchar(30)
	-- ctgr_lclas_nm 카테고리_대분류_nm varchar(30)
	-- ctgr_mclas_id 카테고리_중분류_id 
	-- ctgr_lmclas_nm 카테고리_중분류_nm
	-- collect_dt: 등록 timestamp / 2021-12-14 13:47:50
"""



# python3 crawler.py --date 20211214 --gender f --age 1
# 연령대 > 숫자 / 성별 > 숫자로 입력받도록
parser = argparse.ArgumentParser(description="Command-line에서 성별, 연령, 날짜 반환")
# parser.add_argument("--x", "-x", required=True, help="x값 입력, 형식 : integer")

parser.add_argument(
    "--age",
    "-a",
    required=True,
    help="탐색 연령대 입력,(1:10대/2:20,30대/3:40,50,60대/), 형식 : integer",
)
parser.add_argument("--start_date", "-s", required=True, help="시작일자를 입력받습니다. ex) 20211208")
parser.add_argument("--end_date", "-e", required=True, help="종료일자를 입력받습니다. ex) 20211208")

parser.add_argument(
    "--gender",
    "-g",
    required=True,
    help="탐색하고자하는 성별 입력(1: 남성, 2:여성), 형식 : integer",
)

args = parser.parse_args()

age = int(args.age)
gender = int(args.gender)
start_date = str(args.start_date)
end_date = str(args.end_date)

age_dict = {1: "10대", 2: "20/30대", 3: "40/50/60대"}
gender_dict = {1: "여성", 2: "남성"}

print("탐색 연령 : ", age_dict.get(age), "탐색 성별 : ", gender_dict.get(gender))


# 시작일
#start_date = datetime.datetime.now() - datetime.timedelta(days=1)
#start_date = start_date.strftime("%Y%m%d")
# 시작일
start_yy = int(start_date[0:4])
start_mm = int(start_date[4:6])
start_dd = int(start_date[6:8])



# 종료일
#end_date = datetime.datetime.now() - datetime.timedelta(days=2)
#end_date = end_date.strftime("%Y%m%d")

# 종료일
end_yy = int(end_date[0:4])
end_mm = int(end_date[4:6])
end_dd = int(end_date[6:8])


# 시작, 종료일 확인 출력
print("시작일 : ", end_date)
print("종료일 : ", start_date)


# 금일 출력
todaydate = datetime.datetime.now()
todaydate = todaydate.strftime("%Y-%m-%d")

# 분류할 카테고리 정리
# 카테고리 YN 이 Y인것만
category_lv2 = pd.read_excel("/var/lib/airflow/workspace/tony/src/category_lv3.xlsx")
# category_lv2=category_lv2[category_lv2['YN']=='Y'].reset_index(drop=True)
category_lv2

display = Display(visible=0, size=(1920, 1080))
display.start()

##andrew 기반 tony 수정본 ####### 211209 - cat2id 오수집 수정
keyword_df = pd.DataFrame()
#Headless Option 추가
# 옵션 생성
'''

# 창 숨기는 옵션 추가
options.add_argument("headless")
'''
#에이전트 추가 > 봇으로 인식하여 크롤링이 막힌 경우 주석 해제
#headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
options = webdriver.ChromeOptions()
options.add_argument('User-Agent=Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36')

path = '/var/lib/airflow/workspace/tony/chromedriver'
driver = webdriver.Chrome(path)
driver.implicitly_wait(2)
#time.sleep
url = 'https://datalab.naver.com/shoppingInsight/sCategory.naver'
#time.sleep(0.5)
driver.get(url)
#time.sleep(0.5)

# 기기별 전체 선택
driver.find_element_by_xpath('//*[@id="18_device_0"]').click()
#time.sleep(0.5)
'''
# 성별 여성 선택
driver.find_element_by_xpath('//*[@id="19_gender_1"]').click()
#time.sleep(0.5)
'''


if gender== 1 :
    # 여성 버튼 클릭
    driver.find_element_by_xpath('//*[@id="19_gender_1"]').click()
    #time.sleep(0.5)

elif gender== 2 :
    # 남성 버튼 클릭
    driver.find_element_by_xpath('//*[@id="19_gender_2"]').click()
    #time.sleep(0.5)


# 연령구분 age 변수 입력받기 10 / 2030 / 405060 > 1 /2 / 3


if age == 1:
    #10대버튼 클릭
    driver.find_element_by_xpath('//*[@id="20_age_1"]').click()
    #time.sleep(0.5)

elif age == 2:
    #20대버튼 클릭
    driver.find_element_by_xpath('//*[@id="20_age_2"]').click()
    #time.sleep(0.5)
    #30대버튼 클릭
    driver.find_element_by_xpath('//*[@id="20_age_3"]').click()
    #time.sleep(0.5)   

elif age == 3:
    #40대버튼 클릭
    driver.find_element_by_xpath('//*[@id="20_age_4"]').click()
    #time.sleep(0.5)
    #50대버튼 클릭
    driver.find_element_by_xpath('//*[@id="20_age_5"]').click()
    #time.sleep(0.5)
    #60대버튼 클릭
    driver.find_element_by_xpath('//*[@id="20_age_6"]').click()
    #time.sleep(0.5)

'''
driver.find_element_by_xpath('//*[@id="20_age_4"]').click()
#time.sleep(0.5)
driver.find_element_by_xpath('//*[@id="20_age_5"]').click()
#time.sleep(0.5)
driver.find_element_by_xpath('//*[@id="20_age_6"]').click()
'''

# 종료기간 설정 li[숫자] 만 변경하면 됨 -> 종료기간을 먼저 설정하는게 나을듯
# 1년
driver.find_element_by_xpath('//*[@id="content"]/div[2]/div/div[1]/div/div/div[2]/div[1]/span/label[3]').click()
#time.sleep(0.5)

# 시작일과 연관되어 일 세부를 7로 해주면됨.
driver.find_element_by_xpath('//*[@id="content"]/div[2]/div/div[1]/div/div/div[2]/div[2]/span[3]/div[2]/span').click() # 월
#time.sleep(0.5)
# driver.find_element_by_xpath('//*[@id="content"]/div[2]/div/div[1]/div/div/div[2]/div[2]/span[3]/div[2]/ul/li[5]/a').click() # 월 세부
driver.find_element_by_xpath('//*[@id="content"]/div[2]/div/div[1]/div/div/div[2]/div[2]/span[3]/div[2]/ul/li[' + str(start_mm) + ']/a').click() # 월 세부
#time.sleep(0.5)
 
driver.find_element_by_xpath('//*[@id="content"]/div[2]/div/div[1]/div/div/div[2]/div[2]/span[3]/div[3]/span').click() # 일
#time.sleep(0.5)
driver.find_element_by_xpath('//*[@id="content"]/div[2]/div/div[1]/div/div/div[2]/div[2]/span[3]/div[3]/ul/li[' + str(start_dd) + ']/a').click() # 일 세부

# 시작기간 설정 li[숫자] 만 변경하면 됨 -> 2021년 5월 25일 이런식으로 입력하면 뽑을 수 있도록
driver.find_element_by_xpath('//*[@id="content"]/div[2]/div/div[1]/div/div/div[2]/div[2]/span[1]/div[1]/span').click() # 연
#time.sleep(0.5)
driver.find_element_by_xpath('//*[@id="content"]/div[2]/div/div[1]/div/div/div[2]/div[2]/span[1]/div[1]/ul/li[5]/a').click() # 연 세부 2021년
#time.sleep(0.5)
driver.find_element_by_xpath('//*[@id="content"]/div[2]/div/div[1]/div/div/div[2]/div[2]/span[1]/div[2]/span').click() # 월
#time.sleep(0.5)
driver.find_element_by_xpath('//*[@id="content"]/div[2]/div/div[1]/div/div/div[2]/div[2]/span[1]/div[2]/ul/li[' + str(end_mm) + ']/a').click() # 월 세부
#time.sleep(0.5)
driver.find_element_by_xpath('//*[@id="content"]/div[2]/div/div[1]/div/div/div[2]/div[2]/span[1]/div[3]/span').click() # 일
#time.sleep(0.5)
driver.find_element_by_xpath('//*[@id="content"]/div[2]/div/div[1]/div/div/div[2]/div[2]/span[1]/div[3]/ul/li[' + str(end_dd) + ']/a').click() # 일 세부

for j,cat2_row in tqdm(category_lv2.iterrows()):
    time.sleep(0.5)
    lv1_num=cat2_row['lv1_num']
    lv2_num=cat2_row['lv2_num']
    
        # 카테고리 설정
    driver.find_element_by_xpath('//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[1]/span').click() # 버튼 클릭 후 1차 카테고리
    time.sleep(0.2)
    driver.find_element_by_xpath('//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[1]/ul/li['+str(lv1_num) + ']/a').click() # 세부카테고리 선택
    time.sleep(0.2)
    driver.find_element_by_xpath('//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[2]/span').click() # 버튼 클릭 후 2차 카테고리
    time.sleep(0.2)
    #time.sleep(0.3)
    print("작업시작 : ",lv1_num, lv2_num)
    url_temp = '//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[2]/ul/li['+ str(lv2_num) +']/a'
    driver.find_element_by_xpath(url_temp).click() # 2차카테고리 선택
    #time.sleep(0.3)
    category = driver.find_element_by_xpath('//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[2]/span').text
    # 조회하기 클릭
    driver.find_element_by_xpath('//*[@id="content"]/div[2]/div/div[1]/div/a').click()

    #1차 카테고리->2차 카테고리의 키워드 순위 조회
    #키워드 순위 총 500개가 페이지별로 20위씩까지 조회가능
    #1~100위까지 수집 계획
    time.sleep(0.5)
    keyword_list = [] #1~100위까지 키워드 넣을 리스트
    #p = 수집할 페이지 수, 테스트를 위해선 1을 수정
    for p in range(0, 5):
        time.sleep(0.5)
        # 인기검색어 가져오기
        should_restart=True
        html=driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        keyword_rank_content = soup.select('#content > div.section_instie_area.space_top > div > div:nth-of-type(2) > div.section_insite_sub > div > div > div.rank_top1000_scroll > ul > li')
        print("페이지 내 키워드 수 :",len(keyword_rank_content), p+1, "페이지")
        time.sleep(0.3)
        if len(keyword_rank_content) == 20:    
            while should_restart: #각 페이지 수집을 위한 안전장치
                page_list=[] #페이지별로 보기, 즉 키워드 20개씩 넣을 리스트; 각 페이지는 20위씩 있음-> 5페이지 조회하면 1~100위까지 볼 수 있어서 위에 range(0,5)로 for loop
                for i in range(1, 21): #1~20,21~40,...,81~100
                    #should_restart =True
                    #while should_restart:
                    keyword_path = f'//*[@id="content"]/div[2]/div/div[2]/div[2]/div/div/div[1]/ul/li[{i}]/a'
                    #page_list=[]
                    if int(driver.find_element_by_xpath(keyword_path).text.split('\n')[0])>100: #100위를 넘어서 101위,102위 ...수집하게 되면 다음 카테고리에서 앞 순위들이 누락됨-> 100위 넘기면 더이상 수집못하게 조건문 걸어놓음
                        should_restart=False # while문 탈출
                        break
                    else:
                        page_list.append(driver.find_element_by_xpath(keyword_path).text)
                #인기검색어 순위가 20개가 되지 않을때 예외처리도 진행해야함    
                if len(page_list)==20 or (driver.find_element_by_xpath(f'//*[@id="content"]/div[2]/div/div[2]/div[2]/div/div/div[2]/span/em').text=='6' and int(driver.find_element_by_xpath(keyword_path).text.split('\n')[0])>100):
                #페이지에서 수집한 상품이 20개가 되었을때, 혹은 페이지 넘버가 6이면서 상품순위는 100위가 넘었을때 수집 멈추게끔        
                    should_restart=False # while문 탈출
                    time.sleep(0.2)
                    for page_keyword in page_list:
                        keyword_list.append(page_keyword) #키워드 리스트에 20개씩 5번 넣어줌->1~100위 리스트 생성
            driver.find_element_by_xpath('//*[@id="content"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/a[2]').click()
            time.sleep(0.2)
        else:
            print("검색어 갯수가 20 미만입니다")
            break
 
    # 카테고리 값 추출
    category = driver.find_element_by_xpath('//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[2]/span').text
    if category not in list(category_lv2['category_2nm']):  #간혹 네이버의 카테고리와 우리의 카테고리 리스트가 안 맞는 경우 존재-> 우리가 설정한 카테고리 리스트에 없는 카테고리면 skip...ex)블루레이
        print(category,'not in list')
        continue
    catid = category_lv2[(category_lv2.lv1_num == lv1_num) & (category_lv2.lv2_num == lv2_num)]['category_2'][j]
     #catid = category_lv2[category_lv2['category_2nm']==category].iloc[0]['category_2']
    #time.sleep(0.1)
    category_1nm = category_lv2[category_lv2['category_2nm']==category].iloc[0]['category_1nm']
    print("수집완료 카테고리 :",category_1nm, category, "cat2num : ", catid)
    df = pd.DataFrame()
    df = pd.DataFrame(list(map((lambda x : x.split('\n')), keyword_list)), columns = ['순위', '인기검색어'])

#    #time.sleep(0.3)
    df['category_2'] = catid
    df['category_2nm'] = category
    df['category_1nm'] = category_1nm
    df['category_1'] = lv1_num
#    #time.sleep(0.3)
    keyword_df=keyword_df.append(df)

    '''category_1nm = category_1nm.replace('/','')
    category = category.replace('/','')
    df.to_csv("/var/lib/airflow/workspace/tony/result/result_{todaydate}_{category}_{age}_{gender}.csv".format(todaydate = todaydate, age = age, gender = gender, category = category), encoding = "utf-8-sig")'''
    print(category, "출력 완료")
    time.sleep(2)
print('수집완료')        

driver.quit()

#수집 완료 후 데이터 프레임 생성
todaydate = datetime.datetime.now()
todaydate = todaydate.strftime("%Y-%m-%d")

todaytime = datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S")


keyword_df['register_dt'] = todaydate
keyword_df['gender'] = gender
keyword_df['age'] = age
keyword_df['collect_dt'] = todaytime

#데이터 조인
#현재는 카테고리 lv2로 되어있으나 추후 카테고리 갱신시 코드 상위 카테고리 변수 정정
new = pd.merge(left = keyword_df , right = category_lv2, how = "left", on = "category_2")

#컬럼 드랍
new.drop(columns=["lv1_num","lv2_num","category_2nm_y"], inplace=True)

#컬럼 이름 변경
new.rename(columns = {"인기검색어":"keyword_nm","순위":"keyword_rank","category_1":"ctgr_lclas_id","category_1nm":"ctgr_lcalas_nm","category_2":"ctgr_mclas_id","category_2nm_x":"ctgr_mclas_nm"}, inplace = True)
new.to_csv("/var/lib/airflow/workspace/tony/result/result_{todaydate}_{age}_{gender}_{s}_{e}.csv".format(todaydate = todaydate, age = age, gender = gender, s = end_date , e = start_date), encoding = "utf-8-sig",index = False)
col_nm = ["keyword"]
   
#기존 CSV 내보내기    
#keyword_df.to_csv('/var/lib/airflow/workspace/tony/result/keyword_top100_{strt}_{end}.csv'.format(cat_1nm=category_1nm,cat=category, strt=start_date, end=end_date, number=j), index = False, encoding = 'utf-8-sig')
print(todaydate, '전처리 데이터 가공 및 csv 추출완료')       

#구동 완료 후 가상디스플레이 프로세스도 종료 시켜야 자원 낭비를 막을 수 있는듯
#구동완료후 현재 램 가용용량확인, 동시진행 혹은 순차 진행 가능 여부 확인해봐야할듯
