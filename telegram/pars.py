import requests
import re
import time
from variables import readfile, savefile, save
from bs4 import BeautifulSoup

from header import bot

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/7.0.540.0 Safari/534.10'
c = 'dc9a69c7c8e40ae747e189e1c646d3f3'

class Bot:
    def registration(self, mail, password, user_agent):
        print('registration')
        self.session = requests.Session()
        self.session.headers = {'User-Agent': user_agent, 'content-type': 'application/x-www-form-urlencoded'}

        data = {
            'mail': mail,
            'p': password,
            's': "Отправить"}

        link_auth = 'https://rivalregions.com/rival/pass'

        r = self.session.post(link_auth, data=data)

        _id = re.search(r'name="id" value="(\d+)"', r.text).group(1)

        token = re.search(r'name="access_token" value="(.+)"', r.text).group(1)

        _hash = re.search(r'name="hash" value="(.+)"', r.text).group(1)

        self.session.get(
        f'https://rivalregions.com/?viewer_id={_id}&id={_id}&gl_number=&gl_photo=&gl_photo_medium=&gl_photo_big=&tmz_sent'
        f'=3&wdt_sent=1008&access_token={token}&hash={_hash}')
        
        print('registration success')
    def __init__(self, mail, password, user_agent, c):
        print('__init__')
        self.c = c
        self.headers = {'User-Agent': user_agent, 'content-type': 'application/x-www-form-urlencoded'}
        self.registration(mail=mail, password=password, user_agent=user_agent)

    def send_money(self, recipient_id, money):
        print('send_money')
        data = {'whom': str(recipient_id), 'type': "0", 'n': str(money), 'c': self.c}

        self.session.post('https://rivalregions.com/storage/donate', data=data)

    def replenishment_chek(self):
        print('replenishment_chek')
        while True:
            time.sleep(5)

            last_data1 = str(readfile('last_data1.txt'))
            last_data2 = str(readfile('last_data2.txt'))

            r = self.session.get(f'https://rivalregions.com/log/index/money?c={self.c}').text
            soup = BeautifulSoup(r, 'lxml')
            list_transfer = soup.find_all('tr', 'list_link')

            for element in list_transfer:
                s1 = element.find('div', class_='log_dates').text
                s1 = s1.replace('Сегодня ', '').replace('Вчера ', '').replace(':', '').replace(' ', '')

                s2 = element.find('td', class_='list_log_m').text

                if not 'Пожертвование:' in s2:
                    continue

                if s1 == '0000':
                    last_data1 = '0000'
                    continue

                s3 = 'https://rivalregions.com/#' + element.find('span', 'results_date dot hov2')['action']

                for i in range(0, 11):
                    try:
                        last_data11 = list_transfer[i].find('div', class_='log_dates').text
                        last_data11 = last_data11.replace('Сегодня ', '').replace('Вчера ', '').replace(':', '')

                        last_data22 = list_transfer[i].find('span', 'results_date dot hov2')['action']
                        last_data22 = 'https://rivalregions.com/#' + last_data22
                        break
                    except TypeError:
                        continue

                if int(s1) == int(last_data1) and str(s3) == str(last_data2):
                    break

                if int(s1) < int(last_data1):
                    break
                
                a = element.find_all('td')[1].text.split('R')[0].replace('.', '')
                
                if a[0] == '-': withdraw = False
                elif a[0] == '+': withdraw = True

                a = a[2:][:-1].replace('.', '')

                b = str(s3)
                
                print('before withdraw')

                if withdraw:
                    #profile_telegram = get_parent_key_by_value(profiles, b)

                    #if profile_telegram == None:
                    #    continue
                    
                    #profiles[profile_telegram]['money'] += int(a)
                    #await bot.send_message(profile_telegram, TEXTS[langues[str(profile_telegram)]]['nice_replenishment'].format(ranks(int(a))))
                    print('Вижу перевод')
            savefile('last_data1.txt', str(last_data11))
            savefile('last_data2.txt', str(last_data22))

RRBot = Bot('powerterli@gmail.com', '1mnFrirx', user_agent, c)

RRBot.replenishment_chek()
