#!/usr/bin/env python
# coding: utf-8

# In[104]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings


# 2022년도 데이터 
# 이용정보 데이터: https://data.seoul.go.kr/dataList/OA-15245/F/1/datasetView.do#

# 달별 데이터에서 2022년 데이터로 합치기

# In[19]:


bike_01 = pd.read_csv('data/서울특별시 공공자전거 이용정보(시간대별)_22.01.csv', encoding='cp949')
bike_02 = pd.read_csv('data/서울특별시 공공자전거 이용정보(시간대별)_22.02.csv', encoding='cp949')
bike_03 = pd.read_csv('data/서울특별시 공공자전거 이용정보(시간대별)_22.03.csv', encoding='cp949')
bike_04 = pd.read_csv('data/서울특별시 공공자전거 이용정보(시간대별)_22.04.csv', encoding='cp949')
bike_05 = pd.read_csv('data/서울특별시 공공자전거 이용정보(시간대별)_22.05.csv', encoding='cp949')
bike_06 = pd.read_csv('data/서울특별시 공공자전거 이용정보(시간대별)_22.06.csv', encoding='cp949')
bike_07 = pd.read_csv('data/서울특별시 공공자전거 이용정보(시간대별)_22.07.csv', encoding='cp949')
bike_08 = pd.read_csv('data/서울특별시 공공자전거 이용정보(시간대별)_22.08.csv', encoding='cp949')
bike_09 = pd.read_csv('data/서울특별시 공공자전거 이용정보(시간대별)_22.09.csv', encoding='cp949')
bike_10 = pd.read_csv('data/서울특별시 공공자전거 이용정보(시간대별)_22.10.csv', encoding='cp949')
bike_11 = pd.read_csv('data/서울특별시 공공자전거 이용정보(시간대별)_22.11.csv', encoding='cp949')
bike_12 = pd.read_csv('data/서울특별시 공공자전거 이용정보(시간대별)_22.12.csv', encoding='cp949')

bike_2022= pd.concat([bike_01, bike_02,bike_03, bike_04, bike_05, bike_06, bike_07, bike_08, bike_09, bike_10, bike_11, bike_12])


# In[20]:


bike_2022


# 결측지 확인 

# In[21]:


bike_2022.isna().sum()


# 사용하고자하는 데이터에는 결측지 없음 

# In[22]:


bike_time=bike_2022.groupby(['대여일자', '대여시간'])['이용건수'].sum()
bike_time = bike_time.reset_index() #인덱스 재 정렬 , 기존 인덱스를 열로
bike_time


# 대여일자에서 년도, 월, 일, 요일, 공휴일 변수 생성
# 대여일시에서 시간 변수 생성

# In[70]:


# 년,월,일,요일 생성
bike_time['대여일자'] = pd.to_datetime(bike_time['대여일자'] )
bike_time['년도'] = bike_time['대여일자'].dt.year
bike_time['월'] = bike_time['대여일자'].dt.month
bike_time['일'] = bike_time['대여일자'].dt.day
bike_time['요일(num)'] = bike_time['대여일자'].dt.dayofweek
bike_time['공휴일'] = 0 #0: 평일 1: 공휴일
# 이번에는 토요일 일요일만 공휴일로 변경하고자 함
bike_time.loc[bike_time['요일(num)'].isin([5,6]),['공휴일']] = 1

bike_time.sample(10)


# 미세먼지 경보 발령 22년도 정보 : https://www.airkorea.or.kr/web/pmWarning?pMENU_NO=115

# In[120]:


#엑셀 파일 불러오기 
conda install -c conda-forge xlrd


# In[312]:


#0-2행까지가 Nan값
dust = pd.read_excel('미세먼지 경보발령.xls', header=3)


# In[313]:


# '발령시간'과 '해제시간'을 날짜와 시간으로 분할
dust['발령시간'] = pd.to_datetime(dust['발령시간'].str.replace(' 24', ' 00'))
dust['발령날짜'] = dust['발령시간'].dt.date
dust['발령시각'] = dust['발령시간'].dt.strftime('%H:%M')

dust['해제시간'] = pd.to_datetime(dust['해제시간'])
dust['해제날짜'] = dust['해제시간'].dt.date
dust['해제시각'] = dust['해제시간'].dt.strftime('%H:%M')

# 결과 확인
print(dust[['발령날짜', '발령시각', '해제날짜', '해제시각']])


# 시간 단위로 경보 발령을 나타냄

# In[314]:


from datetime import datetime, timedelta

new_rows = []
for index, row in dust.iterrows():
    start_time = row['발령시간']
    end_time = row['해제시간']
    
    current_time = start_time
    while current_time <= end_time:
        new_rows.append({
            '지역': row['지역'],
            '권역': row['권역'],
            '항목': row['항목'],
            '경보단계': row['경보단계'],
            '발령날짜': current_time.date(),
            '발령시각': current_time.time(),
        })
        current_time += timedelta(hours=1)

dust = pd.DataFrame(new_rows)


# In[315]:


# 변환 후 시간 추출하여 '시각' 열에 저장
dust['시각'] = dust['발령시각'].apply(lambda x: x.strftime('%H:%M'))
dust = dust.drop(columns='발령시각')


# In[328]:


dust.info()


# In[317]:


dust.isna().sum()


# In[ ]:





# 2022년도 기상청 날씨
# 
# 날씨 데이터 : https://data.kma.go.kr/data/grnd/selectAsosRltmList.do?pgmNo=36&tabNo=1

# In[71]:


weather = pd.read_csv('seoul_weather.csv', encoding='cp949')
weather.head(5)


# 일시에서 시간 일시로 나누기

# In[74]:


weather['일시'] = weather['일시'].astype(str)

weather['날짜'] = weather['일시'].str[:10]  
weather['시간'] = weather['일시'].str[11:13].astype(int)  


# 결측지 확인

# In[322]:


weather.isnull().sum()


# In[323]:


# 날짜 시간으로 정렬 (되어있더라도 확실하게 하기위해 한번 더 정렬)
weather = weather.sort_values(['날짜','시간'])
# 전 값으로 채우기 같은 메소드는 이미 만들어져 있음!! 찾아보기 
weather['기온(°C)'].fillna(method='ffill',inplace = True)
weather['누적강수량(mm)'].fillna(method='ffill',inplace = True)
weather['풍속(m/s)'].fillna(method='ffill',inplace = True)
weather['습도(%)'].fillna(method='ffill',inplace = True)


# In[324]:


weather['날짜'] = pd.to_datetime(weather['날짜'])
#데이터 타입 맞추기 
bike_mg = pd.merge (bike_time, 
                       weather, 
                       left_on =['대여일자', '대여시간'], 
                       right_on = ['날짜', '시간']) #default = inner 
bike_mg.head()


# In[329]:


# 시각 열의 데이터 유형을 문자열에서 정수형으로 변환
dust['시각'] = dust['시각'].astype(int)

# bike_mg의 '대여일자' 열을 datetime으로 변환
bike_mg['대여일자'] = pd.to_datetime(bike_mg['대여일자'])

# dust의 '발령날짜' 열을 datetime으로 변환
dust['발령날짜'] = pd.to_datetime(dust['발령날짜'])

# merge 함수로 병합 시도
bike_mg = pd.merge(bike_mg, dust, left_on=['대여일자', '대여시간'], right_on=['발령날짜', '시각'])


# In[342]:


bike_mg.sample(100)


# In[343]:


bike_mg = bike_mg.drop(['대여일자', '지점','일시','풍향(deg)','현지기압(hPa)','해면기압(hPa)','일사(MJ/m^2)','일조(Sec)','날짜','시간_x','시간_y','시각','지역','권역','항목','발령날짜'], axis = 1)


# In[344]:


#시간 time
bike_mg['시간'] = bike_mg['대여시간'].astype(str) + ':00'


# In[345]:


# 칼럼 선택
bike_mg = bike_mg[['년도', '월', '일', '요일(num)', '공휴일','시간','이용건수','기온(°C)',
       '누적강수량(mm)', '풍속(m/s)','습도(%)','경보단계' ]]

#칼럼명 변경
bike_mg.columns = ['년도','월','일','요일','공휴일','시간','이용건수', '기온', '강수량(mm)','풍속(m/s)','습도(%)','미세먼지 경보단계']


# In[346]:


bike_mg.head()


# In[357]:


bike_mg.isnull().sum()


# In[358]:


bike_mg.info()


# In[362]:


#저장
bike_mg.to_csv('bike_mg.csv', index = False, encoding='utf-8-sig')
#불러오기
bike_mg = pd.read_csv('bike_mg.csv')


# In[363]:


data = bike_mg.copy()


# In[364]:


desc_df = data.describe().T
desc_df


# In[351]:


sns.histplot(data['이용건수'])


# In[352]:


sns.boxplot(data['이용건수'])


# 아웃라이어 조정or제거 

# In[353]:


sns.lineplot(x=data['년도'].map(str) + data['월'].map(str), y=data['이용건수'])

