#!/usr/bin/python

import pymysql

con = pymysql.connect(host='localhost', 
                      user='social', 
                      passwd='socialpassword', 
                      db='socialdb')

try:
    with con.cursor() as cur:
        cur.execute('SELECT * FROM cities')

        rows = cur.fetchall()

        for row in rows:
            print(f'{row[0]} {row[1]} {row[2]}')

finally:
    con.close()

con = pymysql.connect(host='localhost', 
                      user='social', 
                      passwd='socialpassword', 
                      db='socialdb')

city = (9, 'Kiev', 2887000)

try:
    with con.cursor() as cur:
        cur.execute('INSERT INTO cities VALUES(%s, %s, %s)',
                    (city[0], city[1], city[2]))
        con.commit()            

        print('new city inserted')
finally:
    con.close()
