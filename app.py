from selenium import webdriver
from datetime import date, timedelta
import time
import pyautogui
import requests
from bs4 import BeautifulSoup

driver = webdriver.Chrome('C:\Program Files\Google\Chrome\Application\chromedriver.exe')

driver.get('https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=코로나')

time.sleep(1)
driver.find_element_by_xpath('//*[@id="search_option_button"]').click()

time.sleep(1)
driver.find_element_by_xpath('//*[@id="_nx_search_option_date_link"]').click()

# 매월, 매초 구하기
today = date.today()
first_day = today.replace(day=1)

last_day_month_ago = first_day - timedelta(days=1)
first_day_month_ago = last_day_month_ago.replace(day=1)

time.sleep(1)
driver.find_element_by_id("_nx_date_from").click()

time.sleep(1)
pyautogui.write(first_day_month_ago.strftime('%Y%m%d'), interval=0.5)

time.sleep(1)
driver.find_element_by_id("_nx_date_to").click()
time.sleep(1)
pyautogui.write(last_day_month_ago.strftime('%Y%m%d'), interval=0.5)

time.sleep(1)
driver.find_element_by_xpath('//*[@id="snb"]/div/ul/li[2]/div/div[1]/span/button').click()

raw = requests.get('https://search.naver.com/search.naver?&where=news&query=코로나', headers={'User-Agent': 'Mozilla/5.0'}).text
html = BeautifulSoup(raw, 'html.parser')

articles = html.select('.list_news > li')

for article in articles:
    title = article.select_one('a.news_tit').text

    print(title)
