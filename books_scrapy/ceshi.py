from urllib import request
from bs4 import BeautifulSoup
import collections, re, os, sys, pymysql


class biqukan:
    '''
	 This is a main Class, the file contains all documents.
	 One document contains paragraphs that have several sentences
	 It loads the original file and converts the original file to new content
	 Then the new content will be saved by this class
	'''

    def __init__(self):
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19'
        }
        self.base_url = 'https://www.bqkan8.com'
        self.type_list = {
            'xuanhuanxiaoshuo': '玄幻',
            'xiuzhenxiaoshuo': '修真',
            'dushixiaoshuo': '都市',
            'chuanyuexiaoshuo': '穿越',
            'wangyouxiaoshuo': '网游',
            'kehuanxiaoshuo': '科幻',
            'qitaxiaoshuo': '其他',
            'wanben': '完本'
        }

    def get_download_url(self, target_url):
        '''
		get download url
		'''
        charter = re.compile(u'[第弟](.+)章', re.IGNORECASE)
        target_req = request.Request(url=target_url, headers=self.header)
        target_response = request.urlopen(target_req)
        target_html = target_response.read().decode('gbk', 'ignore')
        list_main_soup = BeautifulSoup(target_html, 'lxml')
        chapters = list_main_soup.find_all('div', class_='listmain')
        download_soup = BeautifulSoup(str(chapters), 'lxml')
        novel_name = str(download_soup.dl.dt).split("》")[0][5:]
        flag_name = "《" + novel_name + "》" + "正文卷"
        numbers = (len(download_soup.dl.contents) - 1) / 2 - 8
        download_dict = collections.OrderedDict()
        begin_flag = False
        numbers = 1
        for child in download_soup.dl.children:
            if child != '\n':
                if child.string == u"%s" % flag_name:
                    begin_flag = True
                if begin_flag == True and child.a != None:
                    download_url = "https://www.biqukan.com" + child.a.get('href')
                    download_name = child.string
                    download_dict[download_name] = download_url
                    numbers += 1
        return novel_name + '.txt', numbers, download_dict

    def downloader(self, url):
        '''
		download the text
		'''
        download_req = request.Request(url=url, headers=self.header)
        download_response = request.urlopen(download_req)
        download_html = download_response.read().decode('gbk', 'ignore')
        soup_texts = BeautifulSoup(download_html, 'lxml')
        texts = soup_texts.find_all(id='content', class_='showtxt')
        soup_text = BeautifulSoup(str(texts), 'lxml').div.text.replace('\xa0', '')
        return soup_text

    def writer(self, name, path, text):
        '''
		write to sql
		'''
        host = 'localhost'
        username = 'root'
        password = 'sumuc'
        dbname = 'books'
        db = pymysql.connect(host, username, password, dbname)
        cursor = db.cursor()
        sql = 'insert into '

    def get_url(self, type):
        url = 'https://www.bqkan8.com/{0}/'.format(type)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
        }
        req = request.Request(url=url, headers=headers)
        rep = request.urlopen(req)
        html = rep.read().decode('gbk', 'ignore')
        soup_texts = BeautifulSoup(html, 'lxml')
        lists = soup_texts.find(class_='l bd').ul.find_all('li')
        url_list = [self.base_url + i.find(class_='s2').a.get('href') for i in lists]
        # print(url_list)
        return url_list

    def run(self):
        '''
		program entry
		'''
        # target_url = str(input("请输入小说目录下载地址:\n"))
        for type in self.type_list.keys():
            url_list = self.get_url(type)

            for target_url in url_list:
                name, numbers, url_dict = self.get_download_url(target_url)
                if name in os.listdir():
                    os.remove(name)
                index = 1

                # 下载中
                print("《%s》下载中:" % name[:-4])
                for key, value in url_dict.items():
                    self.writer(key, name, self.downloader(value))
                    sys.stdout.write("已下载:%.3f%%" % float(index / numbers) + '\r')
                    sys.stdout.flush()
                    index += 1

                print("《%s》下载完成！" % name[:-4])


if __name__ == '__main__':
    # biqukan().hello().run()
    a = biqukan()
    a.get_url()
