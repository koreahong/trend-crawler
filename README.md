# 트렌드 분석을 위한 크롤러
## 크롤러 파일 구성
```
category_lv3 : 네이버 쇼핑 기준 카테고리 확인 및 대조를 위한 카테고리 파일
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
