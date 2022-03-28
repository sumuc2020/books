from lxml import etree
import requests
import pymysql

conn = None
cursor = None
id = 0


def get_first(arr):
    return arr[0] if len(arr) else ''


def push_request(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/99.0.4844.84 Safari/537.36 '
    }
    response = requests.get(url=url, headers=headers)
    response.encoding = "utf-8"
    return response.text


def connect_database():
    global cursor, conn
    conn = pymysql.connect(host='localhost', port=3307, user='root',
                           password='sumuc', database='books', charset='utf8')
    # 创建游标
    cursor = conn.cursor()


def disconnect_database():
    global cursor, conn
    cursor.close()
    conn.close()


def get_book_list():
    global cursor, conn, id
    j = range(1, 11)
    for i in j:
        url = 'https://www.17k.com/all/book/2_0_0_0_0_0_0_0_{}.html'.format(i)
        text = push_request(url)
        html = etree.HTML(text)
        divs = html.xpath('/html/body/div[4]/div[3]/div[2]/table/tbody/tr')
        for div in divs:
            leibie = get_first(div.xpath('./td[2]/a/text()'))
            shuming = get_first(div.xpath('./td[3]/span/a/text()'))
            shuming_url = 'https:' + get_first(div.xpath('./td[3]/span/a/@href'))
            zxzhangjie = get_first(div.xpath('./td[4]/a/text()'))
            zishu = get_first(div.xpath('./td[5]/text()'))
            zuozhe = get_first(div.xpath('./td[6]/a/text()'))
            if not shuming: continue

            try:
                sql = 'insert into books_jianjie(leibie, shuming, shuming_url, zxzhangjie, zishu, zuozhe)' \
                      'values (%s, %s, %s, %s, %s, %s)'
                cursor.execute(sql, (leibie, shuming, shuming_url, zxzhangjie, zishu, zuozhe))
                id += 1
                conn.commit()
            except Exception as e:
                print(e)
                conn.rollback()
            get_book_content(shuming_url)


def get_book_content(url):
    global id, conn, cursor
    url = url.replace('book', 'list')
    # url = 'https://www.17k.com/list/3378028.html'
    text = push_request(url)
    # print(url)
    html = etree.HTML(text)
    # print(html)/html/body/div[5]/dl/dd
    dl = html.xpath('/html/body/div[5]/dl')[-1]
    divs = dl.xpath('./dd/a')
    for div in divs:
        zhengwen_url = 'https://www.17k.com' + get_first(div.xpath('./@href'))
        text1 = push_request(zhengwen_url)
        # print(text1)
        html1 = etree.HTML(text1)
        # print(html1)       /html/body/div[4]/div[2]/div[2]/div[1]
        divss = html1.xpath('/html/body/div[4]/div[2]/div[2]/div[1]')
        # print(divss)
        for p in divss:
            book_id = id
            zhangjieming = get_first(p.xpath('./h1/text()'))
            zhengwen = '\n'.join(p.xpath('./div[2]/p/text()'))
            # print(zhengwen)
            if not zhangjieming: continue

            try:
                sql = 'insert into book_content(book_id,zhangjieming,zhengwen) ' \
                      'values (%s,%s,%s)'
                cursor.execute(sql, (book_id,zhangjieming,zhengwen))
                conn.commit()
            except Exception as e:
                print(e)
                conn.rollback()


if __name__ == "__main__":
    connect_database()
    get_book_list()
    disconnect_database()
