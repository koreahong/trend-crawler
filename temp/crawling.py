from selenium import webdriver
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
from selenium import webdriver
import pandas as pd
import openpyxl
from tqdm import tqdm

display = Display(visible=0, size=(1920,1080))
display.start()

path = '/var/lib/airflow/workspace/tony/chromedriver'
driver = webdriver.Chrome(path)
#카테고리 현황 업데이트시 필요한 코드
#필요 변수 준비
num1 = 1 # 2분류 목록 갯수 현황
seg1_name = [] # 1분류 이름
seg1_num = [] # 1분류 항목코드
seg2_name = [] # 2분류 이름
seg2_num = [] # 2분류 항목코드
seg1_cnt = [] # 1분류당 2분류의 갯수 담은 리스트
#페이지 url 작성
category_lists_url = "https://datalab.naver.com/shoppingInsight/sCategory.naver"
#페이지 로딩
driver.get(category_lists_url)
html=driver.page_source
soup = BeautifulSoup(html, 'html.parser')
time.sleep(0.2)
#1분류 영역 갯수
seg1_list = soup.select("#content > div.section_instie_area.space_top > div > div.section.insite_inquiry > div > div > div:nth-of-type(1) > div > div:nth-of-type(1) > ul > li")
len(seg1_list)
#1분류 영역 이름
for listss in seg1_list:
    listss = listss.get_text()
    seg1_name.append(listss)
    
#1분류 영역 항목코드 추출
for num11 in range(0,len(seg1_name)):
        seg1_list = soup.select("#content > div.section_instie_area.space_top > div > div.section.insite_inquiry > div > div > div:nth-of-type(1) > div > div:nth-of-type(1) > ul > li > a")[num11]['data-cid']
        print(seg1_list)
        seg1_num.append(seg1_list)
        num11 = num11+1
#1분류 현시점 갯수 > 12개(1~12)
for num in tqdm(range(1,13)):
    #1분류 상세 클릭
    driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div/div[1]/div/div/div[1]/div/div[1]/span').click()
    time.sleep(0.1)
    #1분류 상세 목록 중 해당 항목 클릭
    areaurl = '//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[1]/ul/li['+str(num)+']/a'
    area1 = driver.find_element_by_xpath(areaurl).click()
    time.sleep(0.1)
    #2분류 영역 클릭
    driver.find_element_by_xpath('//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[2]/span').click()
    time.sleep(0.1)
    #2분류 영역 갯수, 항목이름, 항목코드 추출위한 html 파싱
    html=driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    #2분류 영역 갯수 추출
    seg2_list = soup.select("#content > div.section_instie_area.space_top > div > div.section.insite_inquiry > div > div > div:nth-of-type(1) > div > div:nth-of-type(2) > ul > li")
    print("2분류의 갯수는 : ",len(seg2_list),"개")
    seg1_cnt.append(len(seg2_list))
    #2분류 항목 이름 추출 to seg2_name
    seg2_list = soup.select("#content > div.section_instie_area.space_top > div > div.section.insite_inquiry > div > div > div:nth-of-type(1) > div > div:nth-of-type(2) > ul > li")
    for lists in seg2_list:
        lists = lists.get_text()
        print(lists)
        seg2_name.append(lists)
    #2분류 항목 코드 추출
    for num22 in range(0,len(seg2_list)):
        seg2_list = soup.select("#content > div.section_instie_area.space_top > div > div.section.insite_inquiry > div > div > div:nth-of-type(1) > div > div:nth-of-type(2) > ul > li > a")[num22]['data-cid']
        num22+1
        print(seg2_list)
        seg2_num.append(seg2_list)
    #2분류 상세 클릭
    driver.find_element_by_xpath('//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[2]/span').click()

#카테고리 항목 리스트 정리하는 과정
#딕셔너리 2개


#dictionary = dict(zip(string_list, int_list))
#레벨1 카테고리 당 레벨2 카테고리가 몇개인지 표시하는 딕셔너리
cnt_dict = dict(zip(seg1_name, seg1_cnt))
#레벨1 카테고리 이름과 코드를 매치한 카테고리
code_dict = dict(zip(seg1_name, seg1_num))
#dict.fromkeys(key, value) 이용

#새로운 리스트 정의
category_1 = []
category_1nm = []
category_2 = []
category_2nm = []

#레벨1 키(category_1) = 뽑고
codevalues = list(code_dict.values())

#레벨1 밸류(category_1nm)뽑고
codekeys = list(code_dict.keys())

#레벨1 항목별 갯수 추출
#codecnt = [4, 17, 13, 27, 16, 32, 13, 33, 33, 8, 7, 26]
codecnt = list(cnt_dict.values())

num = 0
for a in codecnt:
    for x in range(a):
        category_1.append(codevalues[num])
        category_1nm.append(codekeys[num])
    num = num+1

category_2 = seg2_num
category_2nm = seg2_name

#lv1_num 컬럼 추가하기
seg1_index = list(range(len(seg1_name)))
seg1_index
for num in range(len(seg1_name)):
    seg1_index[num] = num+1
lv1_num = []
num = 0
for a in codecnt:
    for x in range(a):
        lv1_num.append(seg1_index[num])
    num = num+1
lv1_num

#lv2_num 컬럼 추가하기
lv2_num = []
num = 0
for a in codecnt:
    for x in range(a):
        num = num+1
        lv2_num.append(num)
    num = 0

category_lv3 = pd.DataFrame()
#카테고리 수집 완료 후 카테고리 데이터 DF화
category_lv3['category_1'] = pd.Series(category_1)
category_lv3['category_1nm'] = pd.Series(category_1nm)
category_lv3['category_2'] = pd.Series(category_2)
category_lv3['category_2nm'] = pd.Series(category_2nm)
category_lv3['lv1_num'] = pd.Series(lv1_num)
category_lv3['lv2_num'] = pd.Series(lv2_num)

#정리한 DF csv파일로 내보내기
category_lv3.to_csv('./category_lv3.csv', index=False)