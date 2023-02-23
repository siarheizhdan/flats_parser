import requests
from bs4 import BeautifulSoup
from data import Flat
import re
from datetime import datetime


PARSERNAME = 'edc.sale'


def get_all_last_flats_links(page_from=0, page_to=1):
    first_links = []
    while page_from < page_to:
        resp = requests.get(f'https://edc.sale/ru/by/real-estate/sale/apartments/?lt=list&cur=2&page={page_from}')
        html = BeautifulSoup(resp.content, 'html.parser')
        for a in html.find_all('a', href=True, class_="it-item-title c-shadow-overflow"):
            flat_links.append(a['href'])
        page_from += 1
    ready_links = list(filter(lambda el: 'object' in el, flat_links))
    return ready_links