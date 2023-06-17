import requests
import re
import time
from variables import readfile, savefile, save
from bs4 import BeautifulSoup
from mybot import bot, cursor
from telebot import types
#from func import SqlCommit, ToMatheAccount, MiniConstructor

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/7.0.540.0 Safari/534.10'
c = 'Здесь должен быть c от вашего аккаунта РР (посмотреть: 1) Открываете любую статью; 2) Открываете любую программу для отслеживания HTTP-запросов; 3) Лайкаете статью; 4) Смотрите запросы появившегося пакета с названием "1".'

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

    def replenishment_check(self):
        print('replenishment_chek')

        last_data11 = '0'
        last_data22 = '0'
        while True:
            last_data1 = '0'
            last_data2 = '0'
            if str(readfile('last_data1.txt')) != 'None':
                last_data1 = str(readfile('last_data1.txt'))
                last_data2 = str(readfile('last_data2.txt'))

            r = self.session.get(f'https://rivalregions.com/log/index/money?c={self.c}').text
            with open('r.html', 'w') as f:
                print(r, file = f)
            soup = BeautifulSoup(r, 'lxml')
            with open('soup.html', 'w') as f:
                print(soup, file = f)
            list_transfer = soup.find_all('tr', 'list_link')
            with open('list.html', 'w') as f:
                print(list_transfer, file = f)

            for element in list_transfer:
                s1 = element.find('div', class_='log_dates').text
                s1 = s1.replace('Сегодня ', '').replace('Вчера ', '').replace(':', '').replace(' ', '')
                print('s1 is ', s1)

                s2 = element.find('td', class_='list_log_m').text

                if not 'Пожертвование:' in s2:
                    continue

                if s1 == '0000':
                    last_data1 = '0000'
                    continue

                profile = element.find('span', 'results_date dot hov2')['action']
                s3 = 'https://rivalregions.com/#' + profile
                profile = profile[14:]

                for i in range(0, 11):
                    try:
                        last_data11 = list_transfer[i].find('div', class_='log_dates').text
                        last_data11 = last_data11.replace('Сегодня ', '').replace('Вчера ', '').replace(':', '')
                        print('last data 11 is ', last_data11)

                        last_data22 = list_transfer[i].find('span', 'results_date dot hov2')['action']
                        last_data22 = 'https://rivalregions.com/#' + last_data22
                        print('last data 22 is ', last_data22)
                        break
                    except TypeError:
                        continue

                if int(s1) == int(last_data1) and str(s3) == str(last_data2):
                    break

                if int(s1) < int(last_data1):
                    break
                
                a = element.find_all('td')[1].text.split('R')[0].replace('.', '')
                
                if a[0] == '-':
                    break

                amount = int(a[2:][:-1].replace('.', ''))

                chat_id = SqlCommit(f'SELECT tgid FROM users WHERE rrid = {profile}')
                if len(chat_id) == 0:
                    break

                ToMatheAccount(chat_id[0][0], '✅Ривалы', amount)
                MiniConstructor(chat_id[0][0], f'Баланс успешно пополнен на {amount} ривалов!💹💹💹\n\nНе пополняйте баланс следующую минуту, деньги могут не прийти!')


                #do actions here

                print('Вижу перевод')
            savefile('last_data1.txt', str(last_data11))
            savefile('last_data2.txt', str(last_data22))

            #sms below
            lst_dta1 = '0'
            lst_dta2 = '0'
            lst_dta11 = '0'
            lst_dta22 = '0'
            if str(readfile('lst_dta1.txt')) != 'None':
                lst_dta1 = str(readfile('lst_dta1.txt'))
                lst_dta2 = str(readfile('lst_dta2.txt'))

            r = self.session.get(f'https://rivalregions.com/main/messages?c={self.c}').text
            soup = BeautifulSoup(r, 'lxml')
            msgs = soup.find_all('div', 'mess_lines tc ib hov')

            with open('lst.html', 'w') as f:
                print(msgs, file = f)
            print('lst writed')

            for element in msgs:
                #print(element)

                date = element.find('div', class_='chat_dates').text.replace(':', '')[-4:]

                msg = [text for text in element.stripped_strings][2]

                if msg.isnumeric() != True:
                    break

                code = int(msg)

                if code < 100000 or code > 999999:
                    break

                if date == '0000':
                    lst_dta1 = '0000'
                    continue

                profile = str(element).split('"', 2)[1].split('_', 1)[1]
                link = 'https://rivalregions.com/#slide/profile/' + profile

                for i in range(0, 11):
                    try:
                        lst_dta11 = element.find('div', class_='chat_dates').text.replace(':', '')[-4:]
                        print('last data 11 is ', lst_dta11)

                        lst_dta22 = 'https://rivalregions.com/#slide/profile/' + str(element).split('"', 2)[1].split('_', 1)[1]
                        break
                    except TypeError:
                        continue

                if int(date) == int(lst_dta1) and str(link) == str(lst_dta2):
                    break

                if int(date) < int(lst_dta1):
                    break

                who = SqlCommit(f'SELECT name FROM users WHERE code = {code}')
                if len(who) == 0:
                    break
                
                chat_id = SqlCommit(f'SELECT tgid FROM users WHERE code = {code}')[0][0]
                SqlCommit(f'UPDATE users SET rrid = {profile} WHERE code = {code}')
                SqlCommit(f'UPDATE users SET code = 1 WHERE code = {code}')

                print('chatid', chat_id)
                MiniConstructor(chat_id, 'Аккаунт успешно подтвержден! Теперь вы можете пополнять баланс, отправив желаемую сумму на аккаунт банка: https://m.rivalregions.com/#slide/donate/user/246989401')
                #actions here
                #...


                print('Вижу код')
            savefile('lst_dta1.txt', str(lst_dta11))
            savefile('lst_dta2.txt', str(lst_dta22))

            time.sleep(5)

def SqlCommit(*sql):
    raw = sql[0]
    if sql[0].split(' ', 2)[0] + sql[0].split(' ', 2)[1] == 'SELECTDISTINCT':
        fifth = sql[0].split(' ', 4)[4]
        raw = sql[0].replace(fifth, f'"public"."{fifth}"', 1)
    elif sql[0].split(' ', 1)[0] == 'SELECT':
        fourth = sql[0].split(' ', 4)[3]
        raw = sql[0].replace(fourth, f'"public"."{fourth}"', 1)
        #raw = raw + ' RETURNING *'
    elif sql[0].split(' ', 1)[0] == 'UPDATE':
        second = sql[0].split(' ', 2)[1]
        raw = sql[0].replace(second,  f'"public"."{second}"', 1)
        raw = raw + ' RETURNING *'
    elif sql[0].split(' ', 1)[0] == 'INSERT':
        raw = sql[0] + ' RETURNING *'
    elif sql[0].split(' ', 1)[0] == 'DELETE':
        raw = sql[0] + ' RETURNING *'
    if len(sql) == 2:
        cursor.execute(raw, sql[1])
    else:
        cursor.execute(raw)
    if sql[0].split(' ', 1)[0] == 'ALTER':
        return 1
    return cursor.fetchall()

def ToMatheAccount(tgid, curr, value):
    money = SqlCommit(f"SELECT {curr} FROM users WHERE tgid = %s", (tgid,))
    if IsValidForTransmit(0, money, value) or value > 0:
        value = int(value)
        isnone = SqlCommit(f"SELECT {curr} FROM users WHERE tgid = %s", (tgid,))[0][0]
        if isnone == None:
            SqlCommit(f"UPDATE users SET {curr} = {value} WHERE tgid = %s", (tgid,))
            print('exc work')
        else:
            SqlCommit(f"UPDATE users SET {curr} = {curr} + ({value}) WHERE tgid = %s", (tgid,))
        return True
    return False

def MiniConstructor(userid, text, *buttons):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*buttons)
    msg = bot.send_message(userid, text, reply_markup = markup)
    return 1

def IsValidForTransmit(userid, summa, add, *args):
    if isinstance(add, int) == False:
        if add.isnumeric() == True:
            add = int(add)
        else:
            if userid != 0: MiniConstructor(userid, 'Введенные данные не корректны! Кусь!', *args)
            return False
    if isinstance(summa, list) == True:
        print(summa, add)
        summa = summa[0][0]
        print('And now summa is ', summa)
    if isinstance(summa, str) == True:
        if summa.isnumeric() == True:
            summa = int(summa)
    if summa == None:
        print('exc None, summa is ', summa)
        summa = 0
    print('And now summa is ', summa)
    if summa >= add:
        print('summa is ', summa, add)
        return True
    else:
        if userid != 0: MiniConstructor(userid, 'Такой суммы нет на вашем счете! Кусь!', *args)
    return False

RRBot = Bot('Здесь почта от вашего РР-аккаунта (привязывается через мобильное приложение', 'Пароль от РР-аккаунта (он придет по почте после привязки)', user_agent, c)
