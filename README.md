# 트렌드 분석을 위한 크롤러
## 크롤러 디렉토리 구조
```
├── README.md
├── conf                                            : 설정 파일, 접속정보 등 configuration 파일 저장 경로
│   └── sample.yml
├── crawler                                         : 크롤러 저장 경로
│   ├── crawling_keyword.py
│   └── keyword_goods.py
├── results                                         : 크롤링 결과 저장 경로(차후 S3로 이관 예정)
│   ├── bestprd_data
│   │   └── sample.csv
│   ├── hommoa_data
│   │   └── sample.csv
│   └── keyword_data
│       └── sample.csv
├── src                                             : 크롤링을 위한 사전 파일, 드라이버 등의 저장 경로
│   ├── crawler_base
│   │   ├── category_lv2_업데이트.xlsx
│   │   ├── category_lv3.xlsx
│   │   └── naver_goods_cat.csv
│   └── driver
│       └── chromedriver
├── temp                                            : 임시 저장 경로
│   ├── crawling.py
│   └── notebooks
│       ├── crawler_best100.ipynb
│       ├── crawler_homemoa.ipynb
│       └── crawler_keyword100.ipynb
└── utils                                           : 크롤러에서 공통적으로 사용하는 스크립트 저장 경로
    ├── categorizing.py
    ├── categorizing_keyword.py
    └── to_db.py
```
---
## 네이버 베스트 상품
```
베스트 상품에 존재하는 카테고리만 있는 데이터 생성 필요
크롤링 봇으로 인식 회피 위한 클릭 주기 재설정(time.sleep(1.5))
```
### 데이터 컬럼 구성
```
cat_lg
cat_m
```
-
- 
---
## 네이버 데이터랩-쇼핑인사이트 키워드
## 스크립트 실행 방법
```
터미널 명령어 입력
python3 crawler.py  --gender 1 --age 1
gender 1: 여성 / 2: 남성
age : 1:10대 / 2: 2030 / 3:40+

수집 시점 : 전일 1일 or 전일 ~ 전일 일주일 전(7일)
keyword_1 : 전일
keyword_7 : 전일 일주일

```
## 데이터 컬럼 구성
- keyword_rank
- keyword_nm
- ctgr_mclas_id
- ctgr_mclas_nm
- register_dt
- gender
- age
- collect_dt
- ctgr_lclas_id
- ctgr_lclas_nm
---
## 홈쇼핑모아 데이터
-
-
