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


                    #new part
                    inside_menu_test = inside_menu(search_url)

                    if inside_menu_test == 0:
                        print(link.text)
                        print("")
                        category_inside_menu(search_url)
                        print('##################')



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


def inside_menu(url):

    inside_menu_test = 0
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)

    for inside in soup.findAll('ul', {'class': 'filter-middle cat-anch-main first-cats'}):

        inside_menu_test = 1

        skip_first_two_link = 2

        for inside_list in inside.findAll('a', {'class': 'defaultItem'}):

            if skip_first_two_link <=0:
                href = parse.urljoin('https://www.gittigidiyor.com', inside_list.get('href'))

                database.URL_list.insert(
                    {
                        "search_TITLE": inside_list.text,
                        "search_URL": href
                    }
                )

                print(href)

            else:
                skip_first_two_link -= 1

        print("")
        break;

    return inside_menu_test


def category_inside_menu(url):

    category_inside_menu_test = 0
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)

    for inside in soup.findAll('div', {'id': 'CategoryMenu'}):

        category_inside_menu_test = 1

        for inside_list in soup.findAll('a', {'class': 'bgi-none'}):
            href = parse.urljoin('https://www.gittigidiyor.com', inside_list.get('href'))

            print(inside_list.get('title'))
            print(href)
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@")

            category_inside_menu_test = inside_menu(href)
            if category_inside_menu_test == 0:
                print("")
                print("                                                                                 ERROR !!!")
                print("                                                                                " + href)
                print("")

        print("XXXXXXXXXXXXXXXXXXXXXXX")
        print("")
        break;


menu_finder()
