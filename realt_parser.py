import requests
from bs4 import BeautifulSoup
from data import Flat
import re
from datetime import datetime
import db_client


PARSER_NAME = 'realt'


def get_all_last_flats_links(page_from=0, page_to=1):
    flat_links = []
    while page_from < page_to:
        resp = requests.get(f'https://realt.by/sale/flats/?page={page_from}')
        html = BeautifulSoup(resp.content, 'html.parser')
        for a in html.find_all('a', href=True, class_='teaser-title'):
            flat_links.append(a['href'])
        page_from += 1
    ready_links = list(filter(lambda el: 'object' in el, flat_links))
    return ready_links


def enrich_links_to_flats(links):
    flats = []
    for counter, link in enumerate(links):
        resp = requests.get(link)
        html = BeautifulSoup(resp.content, 'html.parser')
        title = html.find('h1', class_='order-1').text.strip()
        raw_price = html.find('h2', class_='w-full')
        if raw_price is not None:
            price = int(re.sub('[^0-9]', '', raw_price.text.strip()))
        else:
            price = 0
        description = html.find('section', class_='bg-white').text.strip()
        try:
            date = datetime.strptime(html.find('span', class_='mr-1.5').text.strip(), '%d.%m.%Y')
        except Exception as  e:
            date = datetime.now()
        flats.append(Flat(
            link=link,
            title=title,
            price=price,
            description=description,
            date=date,
            reference=PARSER_NAME
        ))
        print(f'Спаршено {counter} из {len(links)}')
    return flats


def save_flats(flats):
    for counter, flat in enumerate(flats):
        print(f'Загружено в базу {counter} из {len(flats)}')
        db_client.insert_flat(flat)


def get_last_flats(page_from=0, page_to=1):
    links = get_all_last_flats_links(page_from, page_to)
    flats = enrich_links_to_flats(links[:10])
    save_flats(flats)

get_last_flats()



