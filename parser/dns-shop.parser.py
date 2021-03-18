import json
from urllib.parse import urljoin
from time import sleep
from bs4 import BeautifulSoup
import requests
import mysql.connector

def get_products(urlTemplate: str) -> list:
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'
    }
    session = requests.session()
    session.headers.update(headers)
    items = []

    def get_page(page):
        itemsLocal = []
        url = urlTemplate % page
        rs = session.get(url)
        data = json.loads(rs.text)
        print(data['html'])
        root = BeautifulSoup(data['html'], 'html.parser')

        for a in root.select('.catalog-product__name'):
            #itemsLocal.append(
                #(a.get_text(strip=True), urljoin(rs.url, a['href']))
            #)
            nameProd = a.get_text(strip=True)
            buyUrl = urljoin(rs.url, a["href"])
            
        return itemsLocal
    nowPage = get_page(1)
    i = 1
    while (nowPage != []):
        items += nowPage
        i += 1
        sleep(1)
        nowPage = get_page(i)
        print(nowPage, i)

    return items


with open("dns-shop.parser.py.json") as cfg:
    configuration = json.load(cfg)
dbconn = mysql.connector.connect(**configuration["database"])

