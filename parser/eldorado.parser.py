import json
from urllib.parse import urljoin
from time import sleep
import requests
import mysql.connector

def get_products(category: str, categoryId: int) -> list:
    cursorSQL = dbconn.cursor()
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'
    }
    session = requests.session()
    session.headers.update(headers)

    offset = 0
    end = 1
    url = f"https://www.eldorado.ru/sem/v3/A408/categories/{category}/products?limit=36&offset=%d&orderField=popular&orderDirection=DESC&smallFacetValues=[]&tags=[]"
    
    getInfoSQL = "SELECT COUNT(*) FROM products WHERE name = \"%s\""
    updateSQL = "UPDATE products SET price = %d, imgUri = \"%s\", buyUri = \"%s\", refreshtime = now() WHERE name = \"%s\""
    insertSQL = f"INSERT INTO products VALUES (NULL, {categoryId}, \"%s\", %d, \"%s\", \"%s\", {SITEID}, now())"
    while offset < end:
        sleep(1)
        rs = session.get(url % offset)
        data = rs.json()
        end = data["totalCount"]
        for prod in data["data"]:
            print(prod)
            cursorSQL.execute(getInfoSQL % prod["name"])
            exist = cursorSQL.fetchall()[0][0]
            imageURL = urljoin("https://www.eldorado.ru", prod["images"][0]["url"])
            buyURL = "https://https://www.eldorado.ru/cat/detail/" + prod["code"]
            if exist > 0:
                print(updateSQL % (prod["price"], imageURL, buyURL, prod["name"]))
                cursorSQL.execute(updateSQL % (prod["price"], imageURL, buyURL, prod["name"]))
            else:
                cursorSQL.execute(insertSQL % (prod["name"], prod["price"], imageURL, buyURL))
            dbconn.commit()
        offset += 36


with open("eldorado.parser.py.json") as cfg:
    configuration = json.load(cfg)
dbconn = mysql.connector.connect(**configuration["database"])

SITEID = configuration["siteid"]
