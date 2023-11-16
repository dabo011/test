from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("http://networksciencelab.com/")

soup = BeautifulSoup(html.read(), "html.parser")

# <h1> 태그 출력
print(soup.h1)

# <h2> 태그로 된 모든 인스턴스
level2headers = soup.find_all("h2")
print(level2headers)

# 볼드나 이태릭 포맷으로 된 모든 인스턴스
formats = soup.find_all(["i", "b", "em", "strong"])
print(formats)

# 특정한 속성(href = "v2.jpg" 같은)을 가진 첫 번째 태그
href = soup.find(href = "v2.jpg")
print(href)

# 모든 하이퍼링크나 첫 번째 링크(딕셔너리 구문이나 tag.get() 함수 사용)
links = soup.find_all("a")
firstLink = links[0]["href"]
# 혹은
firstLink = links[0].get("href")
print(links)
print(firstLink)

