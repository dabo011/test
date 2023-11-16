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
    _text = bsoup.select('#articleBodyContents')[0].get_text().replace('\n', " ")
    btext = _text.replace(
        "// flash 오류를 우회하기 위한 함수 추가 function _flash_removeCallback() {}", "")
    news_detail.append(btext.strip())

    # 신문사
    pcompany = bsoup.select('#footer address')[0].a.get_text()
    news_detail.append(pcompany)

    return news_detail


columns = ['날짜', '신문사', '제목', '내용']
df = pd.DataFrame(columns=columns)

queries = ['코로나', '유한양행']   # url 인코딩 에러는 encoding parse.quote(query)
s_date = "2020.04.01"
e_date = "2020.04.08"
s_from = s_date.replace(".", "")
e_to = e_date.replace(".", "")

# MySQL
connection = pymysql.connect(host='54.175.71.24',
                             port=3306,
                             user='social',
                             passwd='socialpassword',
                             db='socialdb')
cursor = connection.cursor()

for query in queries:
    page = 1

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
                    
                    sql = "insert into `news_articles` (`query`, `pub_date`, `publisher`, `title`, `contents`) values (%s, %s, %s, %s, %s)"
                    print(sql)
                    cursor.execute(
                        sql, (query, news_detail[1], news_detail[3], news_detail[0], news_detail[2]))
                    # cursor.execute(
                    #    sql, ('코로나', '2020.01.01.', '연합뉴스', 'title_test', 'contents_test'))
            except Exception as e:
                print(e)
                continue
            if (len(df) == 1):
                break
        page += 10
        break

connection.commit()

# K-평균 군집 분석
import pandas as pd
from konlpy.tag import Hannanum
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans

hannanum = Hannanum()
#Data = pd.read_csv('data/군집분석데이터.csv', engine="python")
sql = "select query, contents from news_articles"
Data = pd.read_sql_query(sql, connection)
df.rename(columns={"qeury": "검색어", "contents": "기사내용"})
print(Data.head())

# 한나눔 형태소 분석기로 명사만 추출
docs = []
for i in Data['기사내용']:
    docs.append(hannanum.nouns(i))

# 명사들을 띄어쓰기를 붙여서 열거
for i in range(len(docs)):
    docs[i] = ' '.join(docs[i])

# 문서-단어 메트릭스 생성
# https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html
vec = CountVectorizer()
X = vec.fit_transform(docs)
df = pd.DataFrame(X.toarray(), columns=vec.get_feature_names())
print(df)

kmeans = KMeans(n_clusters=3).fit(df)
print(kmeans.labels_)

# PCA 기법으로 차원을 2차원으로 축소한 후 군집 결과를 시각화
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

pca = PCA(n_components=2)
principalComponents = pca.fit_transform(df)
principalDf = pd.DataFrame(data=principalComponents,
                          columns=['principal component 1', 'principal component 2'])
principalDf.index = Data['검색어']
print(principalDf)

plt.scatter(principalDf.iloc[kmeans.labels_==0, 0], 
            principalDf.iloc[kmeans.labels_==0, 1], 
            s=10, c='red', label='cluster1')
plt.scatter(principalDf.iloc[kmeans.labels_==1, 0], 
            principalDf.iloc[kmeans.labels_==1, 1], 
            s=10, c='blue', label='cluster2')
plt.scatter(principalDf.iloc[kmeans.labels_==2, 0], 
            principalDf.iloc[kmeans.labels_==2, 1], 
            s=10, c='green', label='cluster3')
plt.legend()

connection.close()