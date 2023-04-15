from func import *
from header import *

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

URL_TEMPLATE = "https://www.work.ua/ru/jobs-odesa/?page=2"
r = requests.get(URL_TEMPLATE)
soup = bs(r.text, 'html.parser')
vacancies_names = soup.find_all('h2', class_='')
for name in vacancies_names:
    print(name.a['title'])

#<h2 class="">
#<a href="/ru/jobs/771567/" title="Продавець-консультант у роздрібний магазин спортивного харчування, вакансия от 13 апреля 2023">Продавець-консультант у роздрібний магазин спортивного харчування</a>
#</h2>
