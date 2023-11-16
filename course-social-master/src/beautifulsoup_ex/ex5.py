from bs4 import BeautifulSoup
from urllib.request import urlopen

# 문자열에서 soup을 생성
soup1 = BeautifulSoup("<html><head></head><body></body></html>")

# 로컬 파일에서 soup을 생성
soup2 = BeautifulSoup(open("myDoc.html"))

# 웹 문서에서 soup을 생성
# urlopen()이 "http://"를 자동으로 추가하지 않음
soup3 = BeautifulSoup(urlopen("http://www.networksciencelab.com/"))
