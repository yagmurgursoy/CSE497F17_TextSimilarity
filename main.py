import requests
from bs4 import BeautifulSoup
from urllib import parse

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

            #print(href)
            #print(title)
            get_single_item_data(href)

        page += 1

def get_single_item_data(item_url):
    source_code = requests.get(item_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)

    for item_name in soup.find_all('span', {'class':'title'}):
        print(item_name.string)

    #for t in soup.find_all('span'):
    #    text = t.string
    #    print(text)

    print('---------------------')

trade_spider(1)
