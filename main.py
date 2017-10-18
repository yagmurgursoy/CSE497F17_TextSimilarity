import requests
from bs4 import BeautifulSoup
from urllib import parse
import pymongo

uri = "mongodb://HasanCemalKaya:27017"
client = pymongo.MongoClient(uri)
database = client['CSE497']
collection = database['GittiGidiyor']
collectionURL = database['URL_list']

#BASE_URL = 'https://www.gittigidiyor.com/erkek-giyim/takim-elbise-tekli-ceket'
#BASE_URL = 'https://www.gittigidiyor.com/sesli-kitap'


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

        print("XXXXXXXXXXXXXXXXXXXXXXXXXX")
        r = requests.get(url)
        url_test = r.url
        if (url_test == BASE_URL) and (page != 1):
            break
        print(r.url)
        print("XXXXXXXXXXXXXXXXXXXXXXXXXX")

        update_last_crawling_url(url_test)

        for t in soup.find_all('span', {'itemprop': 'name'}): 
            title = t.string
            for l in soup.find_all('a', {'title':title}):
                href = parse.urljoin('https://www.gittigidiyor.com', l.get('href'))

            get_single_item_data(href)

        page += 1

    delete_url_from_data(BASE_URL)


def get_single_item_data(item_url):
    source_code = requests.get(item_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)

    for item_name in soup.find_all('span', {'class':'title'}):
        item_title = item_name.string
        print(item_title)

    for item in soup.find_all('span',{'class':'productId hidden-m'}):
        item_test1 = item.string.split('(#')
        item_test2 = item_test1[1].split(')')
        item_ID = item_test2[0]

        print(item_ID)

    for item_text in soup.find_all('div', {'class':'overflow-content'}):
        item_comment =" ".join((item_text.text).split())


        print(item_comment)

    database.GittiGidiyor.insert(
        {
            "URL": item_url,
            "ID": item_ID,
            "TITLE": item_title,
            "COMMENT": item_comment        }
    )

    print('---------------------')

def read_url_from_data():
    url = ""
    for page in collectionURL.find():
        url = page['search_URL']
        break
    return url

def delete_url_from_data(url):

    collectionURL.remove({"search_URL": url})
    return

def update_last_crawling_url(url):

    collectionURL.remove({"search_TITLE": 'LastCrawlingURL'})

    database.URL_list.insert(
        {
            "search_TITLE": 'LastCrawlingURL',
            "search_URL": url
        }
    )
    return

BASE_URL = read_url_from_data()
trade_spider(100)

