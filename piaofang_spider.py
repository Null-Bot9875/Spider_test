from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pyquery import PyQuery as pq

browser = webdriver.Chrome()


def get_page(url):
    print("?")
def parse_one_page():
    print("?")
def main():
    url = 'https://piaofang.maoyan.com/?ver=normal'
    browser.get(url)
    try:
        items = browser.find_elements_by_css_selector('.canTouch')
        print(items)
        for items in items:
            name = browser.find_element_by_id()
    except BaseException as e:
        print(e)
    #browser.close()
if __name__ == '__main__':
    main()
    browser.close()