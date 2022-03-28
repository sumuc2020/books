from lxml import etree
import requests
import pymysql
from books_jianjie import

conn = pymysql.connect(host='localhost', port=3307, user='root',
                       password='sumuc', database='books', charset='utf8')
# 创建游标
cursor = conn.cursor()

try:
    sql = 'select shuming_url from books_jianjie'
    cursor.execute(sql)
    print(sql)
    conn.commit()
except Exception as e:
    print(e)
    conn.rollback()

cursor.close()
conn.close()
