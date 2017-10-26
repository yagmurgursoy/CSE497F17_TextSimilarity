import urllib
from urllib import parse
import requests
from bs4 import BeautifulSoup
import pymongo

uri = "mongodb://HasanCemalKaya:27017"
client = pymongo.MongoClient(uri)
database = client['CSE497']
collection = database['URL_list']

BASE_URL = 'https://www.gittigidiyor.com/'

def menu_finder():

    url_oku = urllib.request.urlopen(BASE_URL)
    soup = BeautifulSoup(url_oku, 'html.parser')

    test = 0

    for menu in soup.find_all('ul',{'class':'megaSublink'}):
        test += 1
        for link in menu.find_all('a'):
            if test < 10:
                search_url = parse.urljoin('https://www.gittigidiyor.com', link.get('href'))

                if link.text != "Markalar" and link.text !="Moda" and link.text !="Kozmetik & Kişisel Bakım" and link.text !="Bebek & Çocuk" \
                        and link.text !="Spor & Outdoor" and link.text !="Ev & Yaşam" and link.text !="Teknoloji":
                    database.URL_list.insert(
                        {
                            "search_TITLE": link.text,
                            "search_URL": search_url
                        }
                    )

                print(link.text)
                print(search_url)

    first_url = ""
    for page in collection.find():
        first_url = page['search_URL']
        break

    database.URL_list.insert(
        {
            "search_TITLE": 'LastCrawlingURL',
            "search_URL": first_url
        }
    )
    for page in collection.find():
        collection.remove({"search_TITLE" : page["search_TITLE"]})
        break

menu_finder()
