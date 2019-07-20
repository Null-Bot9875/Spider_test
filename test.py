import requests
import pymysql
import json
from pyquery import PyQuery as pq

# 使用正则表达式爬取猫眼电影的top100
db = pymysql.connect(host='localhost', user='root', password='root', port=3306, db='spider')


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

    items = doc('tr').items()
    #print(items)
    for item in items:
        name = item.find('.gray-bg').text()
        if len(name) ==0:
            name = item.find('.graybg2').text()

        real_time_money = item.find('.bgcolor2').text()
        if len(real_time_money) ==0:
            real_time_money = item.find('.bgc2').text()

        total_money = item.find('.bgcolor3').text()
        if len(total_money) == 0:
            total_money = item.find('.bgc3').text()

        percent = item.find('.bgcolor4').text()
        if len(percent) == 0:
            percent = item.find('.bgc4').text()

        total_times = item.find('.bgcolor5').text()
        if len(total_times) == 0:
            total_times = item.find('.bgc5').text()

        release_time = item.find('.bgcolor6').text()
        if len(release_time) == 0:
            release_time = item.find('.bgc6').text()

        yield {
                'name': name,
                'real_time_money': real_time_money,
                'total_money': total_money,
                'percent': percent,
                'total_times':total_times,
                'release_time':release_time
            }

def write_to_mysql(item):
    cursor = db.cursor()
    sql = 'INSERT INTO piaofang VALUES (0,"{0}","{1}","{2}","{3}","{4}","{5}");'.format(item['name'],item['real_time_money'],item['total_money'],item['percent'],item['total_times'],item['release_time'])
    try:
        # print(sql)
        cursor.execute(sql)
    except BaseException as e:
        print(e)
        db.rollback()
    db.commit()


def main():
    url = 'http://www.piaofang168.com/'
    html = get_one_page(url)
    # print(html)
    #parse_one_page_1(html)
    for item in parse_one_page(html):
        #print(item)
        write_to_mysql(item)


if __name__ == '__main__':
    main()
    db.close()