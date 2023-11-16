import pymysql
import os

MYSQL_HOST = os.environ.get('', 'localhost')
print(MYSQL_HOST)

con = pymysql.connect(host=MYSQL_HOST,
                       port=3306,
                       user='social',
                       passwd='socialpassword',
                       db='socialdb')