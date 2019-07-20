import requests
import pymysql
import json
from pyquery import PyQuery as pq
# 使用正则表达式爬取猫眼电影的top100
db = pymysql.connect(host='localhost',user='root',password='root',port=3306,db='spider')
def get_one_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'

    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except BaseException as e:
        print(e, +"错误异常码为" + str(response.status_code))


def parse_one_page(html):
    doc = pq(html)
    
    items = doc('.board-item-main').items()
    # print(items)
    for item in items:
        name = item.find('a').text()
        star = str(item.find('.star').text())[3:]
        releasetime = str(item.find('.releasetime').text())[5:15]
        score = item.find('.score').text()
        yield {
            'name': name,
            'star': star,
            'releasetime': releasetime,
            'score': score
        }

def write_to_mysql(item):
    cursor = db.cursor()
    sql = 'INSERT INTO maoyan(id,name,star,releasetime,score) VALUES (0,"{0}","{1}","{2}","{3}");'.format(item['name'],item['star'],item['releasetime'],item['score'])
    try:
        #print(sql)
        cursor.execute(sql)
    except BaseException as e:
        print(e)
        db.rollback()
    db.commit()
def main(offset):
    url = 'https://maoyan.com/board/4' + '?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        write_to_mysql(item)
        #print(item)
if __name__ == '__main__':
    for i in range(10):
        offset = i * 10
        main(offset)
    db.close()