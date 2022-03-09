from lxml import etree
import requests


def get():
    url = 'https://www.readnovel.com/free/all'

    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}

    params = {
        'pageSize': 10,
        'gender': 2,
        'catId': -1,
        'isFinish': -1,
        'isVip': 1,
        'size': -1,
        'updT': -1,
        'orderBy': 0,
        'pageNum': 1
    }

    session = requests.session()

    response = session.get(url=url, headers=headers, params=params)

    html = etree.HTML(response.text)
    print(response.text)

    divs = html.xpath('//*[@id="free-channel-wrap"]/div/div/div[2]/div[2]/div[1]')
    for div in divs:
        book_name = div.xpath('./ul/li[]/div[2]/h3/a/text()')
        print(book_name)
        # print(div)


class person:

    def __init__(self, name=1, age=2):
        self.name = name
        self.age = age

    def print_info(self):
        print(self.name, self.age)

if __name__ == '__main__':
    a = person('sb',18)
    a.print_info()

