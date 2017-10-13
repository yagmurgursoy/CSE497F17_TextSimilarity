import requests
from bs4 import BeautifulSoup
from urllib import parse
import pymongo

uri = "mongodb://HasanCemalKaya:27017"
client = pymongo.MongoClient(uri)
database = client['CSE497']
collection = database['GittiGidiyor']

BASE_URL = 'https://www.gittigidiyor.com/erkek-giyim/takim-elbise-tekli-ceket'

def trade_spider(max_pages):
    page = 1

    while page <= max_pages:
        if page > 1:
            url = BASE_URL + '?sf=' + str(page)
        else:
            url = BASE_URL
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text)

        for t in soup.find_all('span', {'itemprop': 'name'}): 
            title = t.string
            for l in soup.find_all('a', {'title':title}):
                href = parse.urljoin('https://www.gittigidiyor.com', l.get('href'))

            get_single_item_data(href)

        page += 1

def get_single_item_data(item_url):
    source_code = requests.get(item_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)

    for item_name in soup.find_all('span', {'class':'title'}):
        item_title = item_name.string
        print(item_title)

    for item_text in soup.find_all('div', {'class':'overflow-content'}):
        item_comment =" ".join((item_text.text).split())


        print(item_comment)

    database.GittiGidiyor.insert(
        {
            "URL": item_url,
            "TITLE": item_title,
            "COMMENT": item_comment
            # "COMMENT":  " ".join(item_comment.split())
        }
    )

    print('---------------------')


trade_spider(1)
