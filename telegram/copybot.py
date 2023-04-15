from header import *
from func import *

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    PATH_TO_ACCOUNT = f'users/{message.from_user.username}'
    if message.text == 'Мой аккаунт':
        user = SqlCommit('''SELECT * FROM users WHERE name = ?;''', (message.from_user.username,))
        if len(user) == 0:
            with open('announce', "r") as f:
                announce = f.read()

            RRCode = randint(100000, 999999)
            SqlCommit('''INSERT INTO users(name, code, ✅Ривалы, Хостел_Коины) VALUES( ?, ?, ?, ? );''', (message.from_user.username, RRCode, 100, 100))
            user = SqlCommit('''SELECT * FROM users WHERE name = ?;''', (message.from_user.username,))
            info = user[0]
            a = ''
            b = ''
            if info[2] != None: a = 'RRID: ' + str(info[2]) + '\n'
            if info[4] != None: b = 'Эмитент: ' + str(info[4]) + '\n\n'
            info = info[1] + '\n' + a + b

            accounts = []
            for curr in GetAllCurrencies():
                number = str(SqlCommit(f'SELECT {curr} FROM users WHERE name = ?;', ('TerliPower',))[0][0])
                accounts.append(curr + ': ' + number)
            accounts = '\n'.join(accounts)

            MiniConstructor(message.from_user.id, announce + '🤵' + info + '\n' +  accounts, 'Перевести', 'Внести Ривалы', 'Вывести Ривалы', 'Главное меню')
        else:
            with open('announce', "r") as f:
                announce = f.read()

            user = SqlCommit('''SELECT * FROM users WHERE name = ?;''', (message.from_user.username,))
            info = user[0]
            a = ''
            b = ''
            if info[2] != None: a = 'RRID: ' + str(info[2]) + '\n'
            if info[4] != None: b = 'Эмитент: ' + str(info[4]) + '\n\n'
            info = info[1] + '\n' + a + b

            accounts = []
            for curr in GetAllCurrencies():
                number = str(SqlCommit(f'SELECT {curr} FROM users WHERE name = ?;', ('TerliPower',))[0][0])
                accounts.append(curr + ': ' + number)
            accounts = '\n'.join(accounts)

            MiniConstructor(message.from_user.id, announce + '🤵' + info + '\n' + accounts, 'Перевести', 'Внести Ривалы', 'Вывести Ривалы', 'Главное меню')

    elif message.text == '/start':
        MiniConstructor(message.from_user.id, 'Привет, что вы хотите проверить?', 'Мой аккаунт', 'Биржа', 'Топ', 'Настройки')

    elif message.text == 'Перевести' and exists(PATH_TO_ACCOUNT):
        MenuConstructor(message.from_user.id, [0], TransmitMoney0, 'Выберите ценную бумагу', *tuple(GetAllCurrencies()), 'Главное меню')

    elif message.text == 'Главное меню':
        if exists(PATH_TO_ACCOUNT):
            MiniConstructor(message.from_user.id, 'Вы в главном меню, ня', 'Мой аккаунт', 'Биржа', 'Банк', 'Топ', 'Настройки')
        else:
            MiniConstructor(message.from_user.id, 'Вы в главном меню, ня', 'Мой аккаунт', 'Биржа', 'Топ', 'Настройки')

    elif message.text == 'Внести Ривалы' and exists(PATH_TO_ACCOUNT):
        if IsThere(PATH_TO_ACCOUNT, 'RRID') == False:
            MiniConstructor(message.from_user.id, f'Ваш аккаунт Телеграм не привязан к аккаунту Ривал Регионс. Верифицируйте ваш аккаунт, прислав ваш код верификации {GetMarkKey(PATH_TO_ACCOUNT,"RRCode")[:-1]} сообщением на аккаунт банка: https://m.rivalregions.com/#messages/246989401 и подождите принятия заявки, ня', 'Перевести', 'Внести Ривалы', 'Вывести Ривалы', 'Главное меню')
        else:
            MiniConstructor(message.from_user.id, 'Чтобы пополнить свой счет переведите желаемую сумму Ривалов на аккаунт банка: https://m.rivalregions.com/#slide/donate/user/246989401 и ожидайте поступления средств на ваш счет здесь (зачисления происходят вручную)', 'Перевести', 'Внести Ривалы', 'Вывести Ривалы', 'Главное меню')

    elif message.text == 'Вывести Ривалы' and exists(PATH_TO_ACCOUNT):
        if IsThere(PATH_TO_ACCOUNT, 'RRID') == False:
            MiniConstructor(message.from_user.id, f'Ваш аккаунт Телеграм не привязан к аккаунту Ривал Регионс. Верифицируйте ваш аккаунт, прислав ваш код верификации {GetMarkKey(PATH_TO_ACCOUNT,"RRCode")[:-1]} сообщением на аккаунт банка: https://m.rivalregions.com/#messages/246989401 и подождите принятия заявки, ня', 'Перевести', 'Внести Ривалы', 'Вывести Ривалы', 'Главное меню')
        else:
            myorders = []
            with open('orders', 'r') as f:
                lines = f.readlines()
            for line in lines:
                if line.split(' ', 1)[1].split(' ', 1)[0] == message.from_user.username:
                    buf = line.split(' ', 3)
                    myorders.append('№' + buf[0] + '  💲Ривалы: ' + buf[3])
            myorders = '\n'.join(myorders)
            if len(myorders) != 0:
                myorders = 'Ваши заявки на вывод:\n' + '---------------------------------------------\n' + myorders + '=============================================='
                MenuConstructor(message.from_user.id, [0], OrderHandler1, myorders + '\nЖелаете создать новую заявку на вывод или желаете снять заявку с вывода?', 'Вывести', 'Снять заявку')
            else:
                MenuConstructor(message.from_user.id, [0], OrderHandler, 'Введите желаемую к выводу сумму Ривалов и ожидайте их зачисления на свой аккаунт в Ривал Регионс. Вывод осуществляется вручную')

    elif message.text == 'Биржа':
        if exists(PATH_TO_ACCOUNT):
            with open('exchange', "r") as f:
                text = f.readlines()
            a = 0
            for line in text:
                if line.strip():
                    print('exc work')
                    fname = line.split('   ', 1)[1].split('   ', 1)[0]
                    print(fname)
                    if fname == message.from_user.username:
                        print('second if is work')
                        a = 1
                        break
            text = ' '.join(text)
            if a == 0:
                MiniConstructor(message.from_user.id, text, 'Купить', 'Выставить', 'Главное меню') 
            else:
                MiniConstructor(message.from_user.id, text, 'Купить', 'Выставить', 'Снять', 'Главное меню')
        else:
            with open('exchange', "r") as f:
                    text = f.read()
            MiniConstructor(message.from_user.id, text, 'Главное меню')

    elif message.text == 'Выставить' and exists(PATH_TO_ACCOUNT):
        MenuConstructor(message.from_user.id, [0], ExchangeExhibit, 'Выберите ценную бумагу', *tuple(GetAllCurr(PATH_TO_ACCOUNT)), 'Главное меню')

    elif message.text == 'Купить' and exists(PATH_TO_ACCOUNT):
        MenuConstructor(message.from_user.id, [0], ExchangeBuy, 'Введите номер позиции, которую хотите купить', 'Главное меню')

    elif message.text == 'Снять' and exists(PATH_TO_ACCOUNT):
        MenuConstructor(message.from_user.id, [0], ReturnPos, 'Введите номер вашей позиции', 'Главное меню')

    elif message.text == 'Банк' and exists(PATH_TO_ACCOUNT):
        MiniConstructor(message.from_user.id, 'Вы в банке, ня', 'Эмиссия валюты!', 'Издать облигацию', 'Главное меню')

    elif message.text == 'Эмиссия валюты!' and exists(PATH_TO_ACCOUNT):
        if IsThere(PATH_TO_ACCOUNT, 'Эмитент') == False:
            MenuConstructor(message.from_user.id, [0], CreateCurr, 'Введите название вашей новой валюты', 'Главное меню')
        else:
            curr = GetMarkKey(PATH_TO_ACCOUNT, 'Эмитент')[1:][:-1]
            MenuConstructor(message.from_user.id, [PATH_TO_ACCOUNT, curr], EmisCurr, f'Введите количество валюты {curr}, которое вы хотите выпустить', 'Главное меню')

    elif message.text == 'Издать облигацию' and exists(PATH_TO_ACCOUNT):
        MenuConstructor(message.from_user.id, [0], CreateContract, 'Введите название для вашей облигации')

    elif message.text == 'Настройки':
        keyboard = types.InlineKeyboardMarkup()
        url_button = types.InlineKeyboardButton(text='Написать разработчику', url='t.me/TerliPower')
        keyboard.add(url_button)
        msg = bot.send_message(message.from_user.id, 'Не потеряйтесь во всех этих кнопках! Вы можете написать разработчику, чтобы уведомить о багах или сделать предложение по боту', reply_markup = keyboard)

    elif message.text == 'Топ':
        MiniConstructor(message.from_user.id, GetTop('📃Хостел-коины'), 'Мой аккаунт', 'Биржа', 'Банк', 'Топ', 'Настройки')

    elif message.text == 'Рассчитать' and message.from_user.username == 'TerliPower':
        MenuConstructor(message.from_user.id, [0], AdminAdd, 'Укажите валюту', *tuple(GetAllExistCurr()), 'Главное меню')

    elif message.text == 'Указать' and message.from_user.username == 'TerliPower':
        MenuConstructor(message.from_user.id, [0], AdminSet, 'Укажите ник', 'Главное меню')

    elif message.text == 'Анонс' and message.from_user.username == 'TerliPower':
        MenuConstructor(message.from_user.id, [0], SetAnnounce, 'Напишите анонс', 'Удалить', 'Главное меню')

    elif message.text == 'd':
        print(SqlCommit('SELECT ✅Ривалы FROM users;', ''))

bot.polling(none_stop=True, interval=0) #обязательная для работы бота часть
