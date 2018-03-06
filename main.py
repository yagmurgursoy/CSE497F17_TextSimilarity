import requests
from bs4 import BeautifulSoup
from urllib import parse
import pymongo

uri = "mongodb://HasanCemalKaya:27017"
client = pymongo.MongoClient(uri)
database = client['CSE497']
collection = database['GittiGidiyor']
collectionURL = database['URL_list']
MAX_PAGE = 100

#BASE_URL = 'https://www.gittigidiyor.com/erkek-giyim/takim-elbise-tekli-ceket'
#BASE_URL = 'https://www.gittigidiyor.com/sesli-kitap'

def trade_spider(max_pages):

    a = BASE_URL.find("?sf=")

    if a < 0 :
        page = 1
        home_URL = BASE_URL
    else:
        x = BASE_URL.split("?sf=")
        home_URL = x[0]
        y = int(x[1])
        page = y
    print(page)


    while page <= max_pages:
        if page > 1:
            url = home_URL + '?sf=' + str(page)

        else:
            url = home_URL
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text)

        print("XXXXXXXXXXXXXXXXXXXXXXXXXX")
        r = requests.get(url)
        url_test = r.url
        if (url_test == home_URL) and (page != 1):
            break
        print(r.url)
        print("sssssssssssssssssssssssss")

        update_last_crawling_url(url_test)

        for t in soup.find_all('span', {'itemprop': 'name'}): 
            title = t.string
            for l in soup.find_all('a', {'title':title}):
                href = parse.urljoin('https://www.gittigidiyor.com', l.get('href'))

            try:
                get_single_item_data(href)
            except:
                print('ERROR !!!')
                print('Updating page number...')
                print('x')
                print('x')
                print('x')
                print('x')
                #next_crawling_url_for_error()
                print('x')
                print('x')
                print('x')
                print('x')
                print('Starting crawler...')
                #url = read_url_from_data()

        page += 1

    #delete_url_from_data(BASE_URL)
    #next_crawling_url()


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
            "COMMENT": item_comment
        }
    )

    print('---------------------')

def read_url_from_data():
    #url = ""
    current = collectionURL.find_one({"search_TITLE": 'LastCrawlingURL'})
    url = current['search_URL']

    #for page in collectionURL.find():
    #    url = page['search_URL']
    #    break
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

#####################################################################

def next_crawling_url():
    next_url = ""
    for page in collectionURL.find():
        next_url = page['search_URL']
        break

    delete_url_from_data(next_url)

    update_last_crawling_url(next_url)


    return


#####################################################################
def next_crawling_url_for_error():
    current_data = collectionURL.find_one({"search_TITLE": 'LastCrawlingURL'})
    current_url = current_data['search_URL']

    current_url_split = current_url.split('?sf=')
    if(current_url_split[1]):
        page_number = int(current_url_split[1])
    else:
        page_number = 1

    page_number += 1

    next_url = current_url_split[0] + "?sf=" + str(page_number )


    collectionURL.remove({"search_TITLE": 'LastCrawlingURL'})
    database.URL_list.insert(
        {
            "search_TITLE": 'LastCrawlingURL',
            "search_URL": next_url
        }
    )



#####################################################################

#BASE_URL = read_url_from_data()
#trade_spider(MAX_PAGE)
#

######################################################################


BASE_URL = read_url_from_data()
while(BASE_URL):
    trade_spider(MAX_PAGE)

    next_crawling_url()
    BASE_URL = read_url_from_data()






#while(BASE_URL):
#
#    try:
#        trade_spider(MAX_PAGE)
#        BASE_URL = read_url_from_data()
#    except:
#        print('ERROR !!!')
#        print('Updating page number...')
#        print('x')
#        print('x')
#        print('x')
#        print('x')
#        next_crawling_url_for_error()
#        print('x')
#        print('x')
#        print('x')
#        print('x')
#        print('Starting crawler...')
#        BASE_URL = read_url_from_data()
#
#
