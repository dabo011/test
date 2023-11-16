import requests
from bs4 import BeautifulSoup
import json
import re
import sys
import time
import random
import pandas as pd
import pymysql

def get_news(n_url):
    news_detail = []
    print(n_url)
    breq = requests.get(n_url)
    bsoup = BeautifulSoup(breq.content, 'html.parser')

    # 제목 파싱
    title = bsoup.select('h3#articleTitle')[0].text
    news_detail.append(title)

    # 날짜
    pdate = bsoup.select('.t11')[0].get_text()[:11]
    news_detail.append(pdate)

    # news text
    _text = bsoup.select('#articleBodyContents')[
        0].get_text().replace('\n', " ")
    btext = _text.replace(
        "// flash 오류를 우회하기 위한 함수 추가 function _flash_removeCallback() {}", "")
    news_detail.append(btext.strip())

    # 신문사
    pcompany = bsoup.select('#footer address')[0].a.get_text()
    news_detail.append(pcompany)

    return news_detail


columns = ['날짜', '신문사', '제목', '내용']
df = pd.DataFrame(columns=columns)

query = '코로나'   # url 인코딩 에러는 encoding parse.quote(query)
s_date = "2020.04.01"
e_date = "2020.04.08"
s_from = s_date.replace(".", "")
e_to = e_date.replace(".", "")
page = 1

# MySQL
connection = pymysql.connect(host='localhost',
                             port=3306,
                             user='social',
                             passwd='socialpassword',
                             db='socialdb')

while True:
    time.sleep(random.sample(range(3), 1)[0])
    print(page)

    url = "https://search.naver.com/search.naver?where=news&query=" + query + "&sort=1&field=1&ds=" + s_date + "&de=" + e_date + \
        "&nso=so%3Ar%2Cp%3Afrom" + s_from + "to" + \
        e_to + "%2Ca%3A&start=" + str(page)

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    req = requests.get(url, headers=header)
    print(url)
    cont = req.content
    soup = BeautifulSoup(cont, 'html.parser')

    if soup.findAll("a", {"class": "_sp_each_url"}) == []:
        break

    for urls in soup.findAll("a", {"class": "_sp_each_url"}):
        try:
            if urls.attrs["href"].startswith("https://news.naver.com"):
                print(urls.attrs["href"])
                news_detail = get_news(urls.attrs["href"])
                df = df.append(pd.DataFrame(
                    [[news_detail[1], news_detail[3], news_detail[0], news_detail[2]]], columns=columns))
                print(news_detail)
                cursor = connection.cursor()
                sql = "insert into `news_articles` (`pub_date`, `publisher`, `title`, `contents`) values (%s, %s, %s, %s)"
                print(sql)
                cursor.execute(
                    sql, (news_detail[1], news_detail[3], news_detail[0], news_detail[2]))
                #cursor.execute(
                #    sql, ('2020.01.01.', '연합뉴스', 'title_test', 'contents_test'))
                connection.commit()

                make_wordcloud(news_detail[2])
        except Exception as e:
            print(e)
            continue
        if (len(df) == 1):
            break
    page += 10
    break

connection.close()