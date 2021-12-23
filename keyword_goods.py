import openpyxl
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time
import datetime
import random
from selenium import webdriver
from tqdm import tqdm
from pyvirtualdisplay import Display

category_lv2 = pd.read_excel('/var/lib/airflow/workspace/tony/category_lv3.xlsx')

#카테고리 중 Y로 되어있는 항목 수집
category_lv2=category_lv2[category_lv2['YN']=='Y'].reset_index(drop=True)
category_lv2.head()
display = Display(visible=0, size=(1920,1080))
display.start()
# 쇼핑인사이트 이동
path = '/var/lib/airflow/workspace/tony/chromedriver'
driver = webdriver.Chrome(path)
date = datetime.datetime.now


#카테고리 베스트에 있는 카테고리만 선정


def scroll_down(d):
    last_height=d.execute_script("return document.body.scrollHeight")
    while True:
        d.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        new_height=d.execute_script("return document.body.scrollHeight")
        if new_height==last_height:
            break
        last_height=new_height
print("함수정의완료")


##################최종#################### 클래스 이름 변경본(20211126)-> 잘돌아감

#주로 웹링크와 ul,li, 등의 클래스 이름 변경이 생김-> 코드가 안돌아가면 각각 확인
whole_cat_df=pd.DataFrame()
cat_1=category_lv2['category_1'].unique()
count=0
time.sleep(0.5)
for cat1 in cat_1:
    time.sleep(0.5)
    temp_cat1=category_lv2[category_lv2['category_1']==cat1]
    cat_2=temp_cat1['category_2']
    prd_df = pd.DataFrame()
    for num,cat2 in tqdm(enumerate(cat_2)):
        
        #pathname='https://search.shopping.naver.com/best/category/purchase?categoryCategoryId='+str(cat2)+'&categoryChildCategoryId=&categoryDemo=F05&categoryMidCategoryId='+str(cat2)+'&categoryRootCategoryId='+str(cat1)+'&period=P7D'
        #20211126 전 원본
        pathname='https://search.shopping.naver.com/best/category/purchase?categoryCategoryId='+str(cat2)+'&categoryChildCategoryId=&categoryDemo=F05&categoryMidCategoryId='+str(cat2)+'&categoryRootCategoryId='+str(cat1)+'&chartRank=1&period=P7D'
        #20211126업데이트
        #https://search.shopping.naver.com/best/category/purchase?categoryCategoryId=50000167&categoryChildCategoryId=&categoryDemo=F05&categoryMidCategoryId=50000167&categoryRootCategoryId=50000000&chartRank=1&period=P7D
        path = pathname
        time.sleep(1)
        driver.get(path)
        #<div class="style_footer__3DocH">
        searchTxt=''
        while not searchTxt:
            searchTxt=driver.find_elements_by_class_name('style_footer__3DocH .style_footer_area__9dqvk ') #페이지 마지막 부분까지 가게끔 페이지 마지막 element넣어줌
            for i in range(5):
                scroll_down(driver)
                time.sleep(1)
                print("페이지 스크롤")
        html=driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        keywords = list()
        keyword = list()
        
        #keyword = soup.select('ul > li.productList_item__2qOiU ') #20211126 전 원본
        keyword = soup.select('ul > li.imageProduct_item__2eUgO') #20211126업데이트 , 상품리스트 뽑는 코드임-> ul이 전체 상품들 잡아주고 li로 상품 각각 가리킴, 이때의 li 클래스명 넣어주기
        mid_ls = []
        name_ls = []
        price_ls = []
        num_ls = []
        #link_ls=[]
        print(cat2,': ',len(keyword))
        time.sleep(1)
        #.pc_type .productList_list_goods__3mmmw 
        while 0<=len(keyword)<70 : #20211126업데이트 
            # if cat2 ==50000204:
            #     break
            time.sleep(0.5) #20211126업데이트
            scroll_down(driver)
            html=driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            keywords = list()
            #keyword = list()
            #keyword = soup.select('ul > li.productList_item__2qOiU ') #20211126 전 원본
            keyword = soup.select('ul > li.imageProduct_item__2eUgO')#20211126업데이트 , 상품리스트 뽑는 코드임-> ul이 전체 상품들 잡아주고 li로 상품 각각 가리킴, 이때의 li 클래스명 넣어주기
            ##keyword 부분이 문제가 있는듯-> 원래 상품리스트 (상품 약100개) 뽑아야 하는데 0개씩 잡힘
            if len(keyword)>70:
                print(cat2,': ',len(keyword))
                time.sleep(1)
    for i,data2 in enumerate(keyword):    
        time.sleep(0.5)
        #name = data2.select_one("div.productList_title__1nYWw").get_text().strip() #20211126 전 원본
        
        name = data2.select_one("div.imageProduct_title__3TsP1 ").get_text().strip()
        time.sleep(0.5)#20211126업데이트, 상품명
        #name = re.sub(r'[^0-9]', '', name)
        #price=data2.select_one("div.productList_price__V-8gX > strong").get_text().strip() #20211126 전 원본
        price=data2.select_one("div.imageProduct_price__3vXjm > strong").get_text().strip()#20211126업데이트, 상품 가격
        time.sleep(0.5)
        
        price = re.sub(r'[^0-9]', '', price)
        #rank=rank+1
        
        #if data2.select_one("a.productList_btn_store__2O6sO") is None: #20211126 전 원본
        if data2.select_one("a.imageProduct_btn_store__ZPxXy") is None: #20211126업데이트 
            mid=999
        else:
            #mid=data2.select_one("a.productList_btn_store__2O6sO")["data-i"] #20211126 전 원본
            mid=data2.select_one("a.imageProduct_btn_store__ZPxXy")["data-i"] #20211126업데이트 
        #if data2.select_one("a.productList_btn_store__2O6sO") is None:  #20211126 전 원본
        if data2.select_one("a.imageProduct_btn_store__ZPxXy") is None: #20211126업데이트
            #link=data2.select_one("a.productList_link_item__2-qY0")["href"] #20211126 전 원본
            #.imageProduct_link_item__2i1IN 
            link=data2.select_one("a.imageProduct_link_item__2i1IN")["href"] #20211126업데이트, 구매처 링크
        else:
            #link=data2.select_one("a.productList_btn_store__2O6sO")["href"] #20211126 전 원본
            link=data2.select_one("a.imageProduct_btn_store__ZPxXy")["href"] #20211126업데이트, 구매처링크
        mid_ls.append(mid)
        #rank_ls.append(rank)
        name_ls.append(name)
        price_ls.append(price)
        #link_ls.append(link)
        product_info=pd.DataFrame({'name':name_ls})
        product_info['rank']=product_info.reset_index().index+1
        #product_info=pd.DataFrame({'rank':rank_ls})
        name_Series=pd.Series(name_ls,name='product_name')
        mid_Series=pd.Series(mid_ls,name='mid')
        price_Series=pd.Series(price_ls,name= 'price')
        
        #link_Series=pd.Series(link_ls,name='link')
        product_info=pd.concat([product_info,mid_Series,price_Series],axis=1)

        # 카테고리 / 수집일
        product_info['category_2'] = cat2
        #product_info['date'] = date
        #print(product_info)
        catid = category_lv2[category_lv2['category_2']==cat2].iloc[0]['category_2']
        category_1nm = category_lv2[category_lv2['category_2']==cat2].iloc[0]['category_1nm']
        category_1nm = category_1nm.replace('/','')

        prd_df = prd_df.append(product_info)
        #prd_df.set_index('rank',inplace=True)
        

    whole_cat_df=whole_cat_df.append(prd_df)
    print('**********',cat1,'수집완료**********')

whole_cat_df.to_csv('/var/lib/airflow/workspace/tony/result/test_naver_best100_{date}_practice.csv'.format(date = date), index=False)
print('해당 카테고리 수집 완료')  

whole_cat_df.to_csv('/var/lib/airflow/workspace/tony/result/naver_best100_{date}_practice.csv'.format(date = date), index=False)

#페이지 로딩 후 수집
#페이지 카테고리 이동 후 수집
#스크롤 작업 진행 후 수집
