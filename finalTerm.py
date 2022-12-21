#!/usr/bin/env python
# coding: utf-8

# In[6]:


from selenium import webdriver
import time
from bs4 import BeautifulSoup as bs
import pandas as pd 
from collections import OrderedDict
import numpy as np
import re
import matplotlib.pyplot as plt

 
# 한글 폰트 사용을 위해서 세팅
from matplotlib import font_manager, rc
font_path = "C:/Windows/Fonts/NGULIM.TTF"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font) 

url = 'https://www.melon.com/'
driver = webdriver.Chrome('./chromedriver.exe')
driver.implicitly_wait(10)
driver.get(url)

# selenium 라이브러리로 멜론 페이지 이동
driver.find_element_by_xpath('//*[@id="gnb_menu"]/ul[1]/li[1]/a/span[2]').click()
time.sleep(0.5)

driver.find_element_by_xpath('//*[@id="gnb_menu"]/ul[1]/li[1]/div/ul/li[4]/a/span').click()
time.sleep(0.5)

driver.find_element_by_xpath('//*[@id="cont_wrap"]/div/div/div[3]/div/button').click()
time.sleep(0.5)

driver.find_element_by_xpath('//*[@id="cont_wrap"]/div/div/div[3]/div/div/dl/dt/button[1]').click()
time.sleep(0.5)

driver.find_element_by_xpath('//*[@id="cont_wrap"]/div/div/div[3]/div/div/dl/dd/ul/li[1]').click()
time.sleep(0.5)

# 2021 데이터 GET

list_2021 = ['1','2','3','4','5','6','7','8','9','10','11','12']

# 2021년 데이터 추출 배열
df_list_2021 = []

# 2021년 1위 음원 추출 배열
df_win_2021 = []

# 2021년 월별 좋아요가 많은 음원 추출 배열
df_max_2021 = []

for i in list_2021:
    driver.find_element_by_xpath('//*[@id="cont_wrap"]/div/div/div[3]/div/div/dl/dd/ul/li['+i+']').click()
    time.sleep(0.7)

    html = driver.page_source
    soup = bs(html, 'html.parser')
    song_soup = soup.select('tbody > tr')
    
    song_lst = []

    for song in song_soup:
        song_month = i + '월'
        song_rank = song.find('span', class_= 'rank').get_text()
        song_title = song.find('div', class_= 'ellipsis rank01').get_text()
        song_artist = song.find('span', class_= 'checkEllipsis').get_text()
        song_album = song.find('div', class_= 'ellipsis rank03').get_text()
        song_likes = song.find('button', class_ = 'button_etc like').get_text().replace(',', '')

        # list에 append하면서 쓸데없는 문자, 공백 replace를 통해 삭제
        song_lst.append([song_rank, song_title.replace('\n', ''), 
                         song_artist.replace('\n', ''), song_album.replace('\n', ''), 
                         int(song_likes.replace('\n', '').replace('좋아요총건수', '')), song_month])

    df = pd.DataFrame(song_lst, columns = ['순위', '제목', '가수', '앨범', 'likes','월'])
    df.head(30)
    
    df_list_2021.append(df.head(30))
    
    df_win_2021.append(df.head(1))
    
    df_max_2021.append(df.head(30).sort_values(by=['likes'], ascending=True).drop_duplicates(subset=['likes'], keep='first').head(1))
    
# 2022 데이터 GET
driver.find_element_by_xpath('//*[@id="cont_wrap"]/div/div/div[3]/div/div/dl/dt/button[2]').click()
time.sleep(0.7)

list_2022 = ['1','2','3','4','5','6','7','8','9','10','11']

# 2022년 데이터 추출 배열
df_list_2022 = []

# 2022년 1위 음원 추출 배열
df_win_2022 = []

# 2022년 월별 좋아요가 많은 음원 추출 배열
df_max_2022 = []

for i in list_2022:
    driver.find_element_by_xpath('//*[@id="cont_wrap"]/div/div/div[3]/div/div/dl/dd/ul/li['+i+']').click()
    time.sleep(0.6)

    html = driver.page_source
    soup = bs(html, 'html.parser')
    song_soup = soup.select('tbody > tr')
    
    song_lst = []

    for song in song_soup:
        song_month = i + '월'
        song_rank = song.find('span', class_= 'rank').get_text()
        song_title = song.find('div', class_= 'ellipsis rank01').get_text()
        song_artist = song.find('span', class_= 'checkEllipsis').get_text()
        song_album = song.find('div', class_= 'ellipsis rank03').get_text()
        song_likes = song.find('button', class_ = 'button_etc like').get_text().replace(',', '')
        
        # list에 append하면서 쓸데없는 문자, 공백 replace를 통해 삭제
        song_lst.append([song_rank, song_title.replace('\n', ''), song_artist.replace('\n', ''), song_album.replace('\n', ''), int(song_likes.replace('\n', '').replace('좋아요총건수', '')), song_month])

    df = pd.DataFrame(song_lst, columns = ['순위', '제목', '가수', '앨범', 'likes','월'])
    df.head(30)
    
    df_list_2022.append(df.head(30))
    
    df_win_2022.append(df.head(1))
    
    df_max_2022.append(df.head(30).sort_values(by=['likes'], ascending=True).drop_duplicates(subset=['likes'], keep='first').head(1))

# 월별 좋아요 많은 그래프 만들기
# 2021년 좋아요 1위 음원 엑셀 추출 저장
excel1 = pd.DataFrame.from_records(df_max_2021[0])
excel2 = pd.DataFrame.from_records(df_max_2021[1])
excel3 = pd.DataFrame.from_records(df_max_2021[2])
excel4 = pd.DataFrame.from_records(df_max_2021[3])
excel5 = pd.DataFrame.from_records(df_max_2021[4])
excel6 = pd.DataFrame.from_records(df_max_2021[5])
excel7 = pd.DataFrame.from_records(df_max_2021[6])
excel8 = pd.DataFrame.from_records(df_max_2021[7])
excel9 = pd.DataFrame.from_records(df_max_2021[8])
excel10 = pd.DataFrame.from_records(df_max_2021[9])
excel11 = pd.DataFrame.from_records(df_max_2021[10])
excel12 = pd.DataFrame.from_records(df_max_2021[11])

excel_2021_max = pd.concat([excel1,excel2,excel3,excel4,excel5,excel6,excel7,excel8,excel9,excel10,excel11,excel12])

excel_2021_max.to_csv("2021년도_월별_좋아요_음원.csv", encoding='cp949', index='월')

# 2022년 1위 음원 엑셀 추출 저장
excel1 = pd.DataFrame.from_records(df_max_2022[0])
excel2 = pd.DataFrame.from_records(df_max_2022[1])
excel3 = pd.DataFrame.from_records(df_max_2022[2])
excel4 = pd.DataFrame.from_records(df_max_2022[3])
excel5 = pd.DataFrame.from_records(df_max_2022[4])
excel6 = pd.DataFrame.from_records(df_max_2022[5])
excel7 = pd.DataFrame.from_records(df_max_2022[6])
excel8 = pd.DataFrame.from_records(df_max_2022[7])
excel9 = pd.DataFrame.from_records(df_max_2022[8])
excel10 = pd.DataFrame.from_records(df_max_2022[9])
excel11 = pd.DataFrame.from_records(df_max_2022[10])

excel_2022_max = pd.concat([excel1,excel2,excel3,excel4,excel5,excel6,excel7,excel8,excel9,excel10,excel11])

excel_2022_max.to_csv("2022년도_월별_좋아요_음원.csv", encoding='cp949', index='월')

df = pd.read_csv("2021년도_월별_좋아요_음원.csv", encoding='cp949')
plt.figure(figsize=(20, 5))
plt.bar(np.arange(len(df)),df["likes"])
plt.title('2021년도_월별_좋아요_음원', fontsize=20)
plt.xlabel('음원명', fontsize=18)
plt.ylabel('좋아요 수', fontsize=18)
plt.xticks(np.arange(len(df)), df["제목"], fontsize=10)
plt.xticks(rotation=45)
plt.show()

df = pd.read_csv("2022년도_월별_좋아요_음원.csv", encoding='cp949')
plt.figure(figsize=(20, 5))
plt.bar(np.arange(len(df)),df["likes"])
plt.title('2022년도_월별_좋아요_음원', fontsize=20)
plt.xlabel('음원명', fontsize=10)
plt.ylabel('좋아요 수', fontsize=18)
plt.xticks(np.arange(len(df)), df["제목"], fontsize=10)
plt.xticks(rotation=45)
plt.show()
# 여기까지 월별 좋아요 많은 그래프 만들기

# 엑셀 추출
# 2021년 1위 음원 엑셀 추출 저장
excel1 = pd.DataFrame.from_records(df_win_2021[0])
excel2 = pd.DataFrame.from_records(df_win_2021[1])
excel3 = pd.DataFrame.from_records(df_win_2021[2])
excel4 = pd.DataFrame.from_records(df_win_2021[3])
excel5 = pd.DataFrame.from_records(df_win_2021[4])
excel6 = pd.DataFrame.from_records(df_win_2021[5])
excel7 = pd.DataFrame.from_records(df_win_2021[6])
excel8 = pd.DataFrame.from_records(df_win_2021[7])
excel9 = pd.DataFrame.from_records(df_win_2021[8])
excel10 = pd.DataFrame.from_records(df_win_2021[9])
excel11 = pd.DataFrame.from_records(df_win_2021[10])
excel12 = pd.DataFrame.from_records(df_win_2021[11])

excel_2021 = pd.concat([excel1,excel2,excel3,excel4,excel5,excel6,excel7,excel8,excel9,excel10,excel11,excel12])

excel_2021.to_csv("2021년도_1위_음원.csv", encoding='cp949', index='월')

df = pd.read_csv("2021년도_1위_음원.csv", encoding='cp949')
plt.figure(figsize=(20, 5))
plt.bar(np.arange(len(df)),df["likes"])
plt.title('2021년도_1위_음원', fontsize=20)
plt.xlabel('음원명', fontsize=18)
plt.ylabel('좋아요 수', fontsize=18)
plt.xticks(np.arange(len(df)), df["제목"], fontsize=10)
plt.xticks(rotation=45)
plt.show()

# 2022년 1위 음원 엑셀 추출 저장
excel1 = pd.DataFrame.from_records(df_win_2022[0])
excel2 = pd.DataFrame.from_records(df_win_2022[1])
excel3 = pd.DataFrame.from_records(df_win_2022[2])
excel4 = pd.DataFrame.from_records(df_win_2022[3])
excel5 = pd.DataFrame.from_records(df_win_2022[4])
excel6 = pd.DataFrame.from_records(df_win_2022[5])
excel7 = pd.DataFrame.from_records(df_win_2022[6])
excel8 = pd.DataFrame.from_records(df_win_2022[7])
excel9 = pd.DataFrame.from_records(df_win_2022[8])
excel10 = pd.DataFrame.from_records(df_win_2022[9])
excel11 = pd.DataFrame.from_records(df_win_2022[10])

excel_2022 = pd.concat([excel1,excel2,excel3,excel4,excel5,excel6,excel7,excel8,excel9,excel10,excel11])

excel_2022.to_csv("2022년도_1위_음원.csv", encoding='cp949', index='월')

df = pd.read_csv("2022년도_1위_음원.csv", encoding='cp949')
plt.figure(figsize=(20, 5))
plt.bar(np.arange(len(df)),df["likes"])
plt.title('2022년도_1위_음원', fontsize=20)
plt.xlabel('음원명', fontsize=18)
plt.ylabel('좋아요 수', fontsize=18)
plt.xticks(np.arange(len(df)), df["제목"], fontsize=10)
plt.xticks(rotation=45)
plt.show()
# 여기까지 엑셀 저장

# 크롬 브라이저 종료
driver.quit()

# print("2021년도 1위 음원")
# print(df_win_2021)
# print("-----------")
# print("2022년도 1위 음원")
# print(df_win_2022)


# In[ ]:





# In[ ]:




