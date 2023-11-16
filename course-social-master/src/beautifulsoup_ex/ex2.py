from urllib.request import urlopen
from bs4 import BeautifulSoup

bsObj = BeautifulSoup(open("src/beautifulsoup_ex/ex2.html", encoding='UTF8'))

List = bsObj.find_all("span",{"class":"yellow"})

for i in List:
    print(i.get_text())
