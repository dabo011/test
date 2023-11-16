
from bs4 import BeautifulSoup 
import requests 
import re 
import sys 
import pprint

# 댓글 수집
comment_list = [] 

# 연합뉴스 기사: 15일부터 미세먼지 심한 날 '5등급 차' 서울서 운행 못 한다(종합2보)
article_url = "https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=102&oid=001&aid=0010630211"

oid = article_url.split("oid=")[1].split("&")[0]  # 001
aid = article_url.split("aid=")[1]  # 0010630211
page = 1
header = {
    "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
    "referer": article_url,

}

while True : 
    # 댓글 파싱 단계
    comment_url = "https://apis.naver.com/commentBox/cbox/web_neo_list_jsonp.json?ticket=news&templateId=default_society&pool=cbox5&_callback=jQuery1707138182064460843_1523512042464&lang=ko&country=&objectId=news" + \
        oid + "%2C" + aid + "&categoryId=&pageSize=20&indexSize=10&groupId=&listType=OBJECT&pageType=more&page=" + \
        str(page) + "&refresh=false&sort=FAVORITE"
    
    r = requests.get(comment_url, headers=header)
    content_soup = BeautifulSoup(r.content, "html.parser")
   
    # 댓글을 리스트에 추가
    match = re.findall('"contents":([^\*]*),"userIdNo"', str(content_soup)) # 댓글만 뽑아내기
    comment_list.append(match) 

    # 페이지 당 댓글이 20개씩 보이므로 마지막 페이지까지 도달할 수 있도록 반복 실행
    no_comment = str(content_soup).split('comment":')[1].split(",")[0] # 댓글 개수
    if int(no_comment) <= ((page) * 20): 
        break 
    else :  
        page += 1

# 리스트 평탄화 작업
def flatten(l): 
    flat_list = [] 
    for elem in l: 
        if type(elem) == list: 
            for e in elem: 
                flat_list.append(e) 
        else: 
            flat_list.append(elem) 
    return flat_list

flatten(comment_list)
