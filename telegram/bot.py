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
                number = str(SqlCommit(f'SELECT {curr} FROM users WHERE name = ?;', (message.from_user.username,))[0][0])
                if number == 'None':
                    continue
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
                number = str(SqlCommit(f'SELECT {curr} FROM users WHERE name = ?;', (message.from_user.username,))[0][0])
                if number == 'None':
                    continue
                isdef = ''
                if curr[0] == '📃':
                    qisdef = SqlCommit(f'SELECT isdef FROM bonds WHERE name = ?;', (curr,))[0][0]
                    if qisdef == 1:
                        isdef = ' - дефолт!'
                accounts.append(curr + ': ' + number + isdef)
            accounts = '\n'.join(accounts)

            MiniConstructor(message.from_user.id, announce + '🤵' + info + '\n' + accounts, 'Перевести', 'Внести Ривалы', 'Вывести Ривалы', 'Главное меню')

    elif message.text == '/start':
        MiniConstructor(message.from_user.id, 'Привет, что вы хотите проверить?', 'Мой аккаунт', 'Биржа', 'Топ', 'Настройки')

    elif message.text == 'Перевести' and len(SqlCommit('SELECT * FROM users WHERE name = ?', (message.from_user.username,))) != 0:
        MenuConstructor(message.from_user.id, [0], TransmitMoney0, 'Выберите ценную бумагу', *tuple(GetAllCurrencies()), 'Главное меню')

    elif message.text == 'Главное меню':
        if len(SqlCommit('SELECT * FROM users WHERE name = ?', (message.from_user.username,))) != 0:
            MiniConstructor(message.from_user.id, 'Вы в главном меню, ня', 'Мой аккаунт', 'Биржа', 'Банк', 'Топ', 'Настройки')
        else:
            MiniConstructor(message.from_user.id, 'Вы в главном меню, ня', 'Мой аккаунт', 'Биржа', 'Топ', 'Настройки')

    elif message.text == 'Внести Ривалы' and len(SqlCommit('SELECT * FROM users WHERE name = ?', (message.from_user.username,))) != 0:
        RRID = SqlCommit('SELECT rrid FROM users WHERE name = ?', (message.from_user.username,))[0][0]
        if RRID == None:
            rrcode = SqlCommit('SELECT code FROM users WHERE name = ?', (message.from_user.username,))[0][0]
            MiniConstructor(message.from_user.id, f'Ваш аккаунт Телеграм не привязан к аккаунту Ривал Регионс. Верифицируйте ваш аккаунт, прислав ваш код верификации {rrcode} на аккаунт банка: https://m.rivalregions.com/#messages/246989401 и подождите принятия заявки, ня', 'Перевести', 'Внести Ривалы', 'Вывести Ривалы', 'Главное меню')
        else:
            MiniConstructor(message.from_user.id, 'Чтобы пополнить свой счет переведите желаемую сумму Ривалов на аккаунт банка: https://m.rivalregions.com/#slide/donate/user/246989401 и ожидайте поступления средств на ваш счет здесь (зачисления происходят вручную)', 'Перевести', 'Внести Ривалы', 'Вывести Ривалы', 'Главное меню')

    elif message.text == 'Вывести Ривалы' and len(SqlCommit('SELECT * FROM users WHERE name = ?', (message.from_user.username,))) != 0:
        RRID = SqlCommit('SELECT rrid FROM users WHERE name = ?', (message.from_user.username,))[0][0]
        if RRID == None:
            rrcode = SqlCommit('SELECT code FROM users WHERE name = ?', (message.from_user.username,))[0][0]
            MiniConstructor(message.from_user.id, f'Ваш аккаунт Телеграм не привязан к аккаунту Ривал Регионс. Верифицируйте ваш аккаунт, прислав ваш код верификации {rrcode} сообщением на аккаунт банка: https://m.rivalregions.com/#messages/246989401 и подождите принятия заявки, ня', 'Перевести', 'Внести Ривалы', 'Вывести Ривалы', 'Главное меню')
        else:
            myorders = SqlCommit('SELECT * FROM orders WHERE name = ?', (message.from_user.username,))
            if len(myorders) != 0:
                poses = ''
                for pos in myorders:
                    for element in pos:
                        element = str(element)
                        poses += element + '   '
                    poses = poses[:-3]
                    poses += '\n'

                myorders = 'Ваши заявки на вывод:\n' + '---------------------------------------------\n' + poses + '=============================================='
                MenuConstructor(message.from_user.id, [0], OrderHandler1, myorders + '\nЖелаете создать новую заявку на вывод или желаете снять заявку с вывода?', 'Вывести', 'Снять заявку')
            else:
                MenuConstructor(message.from_user.id, [0], OrderHandler, 'Введите желаемую к выводу сумму Ривалов и ожидайте их зачисления на свой аккаунт в Ривал Регионс. Вывод осуществляется вручную')

    elif message.text == 'Биржа':
        rawpos = SqlCommit(f'SELECT * FROM exchange')
        poses = ''
        for pos in rawpos:
            for element in pos:
                element = str(element)
                poses += element + '   '
            poses = poses[:-3]
            poses += '\n'

        exchange = '№      Продает      Получаете      Отдаете      Резерв\n\n' + poses

        isaccexists = len(SqlCommit(f'SELECT name FROM users WHERE name = ?', (message.from_user.username,))) == 1
        if isaccexists == False:
            MiniConstructor(message.from_user.id, exchange, 'Главное меню')
            return 1

        a = 0
        for pos in rawpos:
            if pos[1] == message.from_user.username:
                a = 1
                break

        if a == 0:
            MiniConstructor(message.from_user.id, exchange, 'Купить', 'Выставить', 'Главное меню')
            return 1
        MiniConstructor(message.from_user.id, exchange, 'Купить', 'Выставить', 'Снять', 'Главное меню')

    elif message.text == 'Выставить' and len(SqlCommit('SELECT * FROM users WHERE name = ?', (message.from_user.username,))) != 0:
        MenuConstructor(message.from_user.id, [0], ExchangeExhibit, 'Выберите ценную бумагу', *tuple(GetAllCurrsUserHas(message.from_user.username)), 'Главное меню')

    elif message.text == 'Купить' and len(SqlCommit('SELECT * FROM users WHERE name = ?', (message.from_user.username,))) != 0:
        MenuConstructor(message.from_user.id, [0], ExchangeBuy, 'Введите номер позиции, которую хотите купить', 'Главное меню')

    elif message.text == 'Снять' and len(SqlCommit('SELECT * FROM users WHERE name = ?', (message.from_user.username,))) != 0:
        MenuConstructor(message.from_user.id, [0], ReturnPos, 'Введите номер вашей позиции', 'Главное меню')

    elif message.text == 'Банк' and len(SqlCommit('SELECT * FROM users WHERE name = ?', (message.from_user.username,))) != 0:
        MiniConstructor(message.from_user.id, 'Вы в банке, ня', 'Эмиссия валюты!', 'Издать облигацию', 'Главное меню')

    elif message.text == 'Эмиссия валюты!' and len(SqlCommit('SELECT * FROM users WHERE name = ?', (message.from_user.username,))) != 0:
        money = SqlCommit('SELECT Хостел_Коины FROM users WHERE name = ? ;', (message.from_user.username,))[0][0]
        isemitent = SqlCommit('SELECT emitent FROM users WHERE name = ? ;', (message.from_user.username,))[0][0]
        print(isemitent)
        if isemitent != None:
            MenuConstructor(message.from_user.id, [message.from_user.username, isemitent], EmisCurr, f'Издание валюты {isemitent} вам обойдется в 1 Хостел-Коин за каждую бумагу. Вы можете издать {money} бумаг\n\nВведите желаемое количество', 'Главное меню')
            return 1
        if money < 11:
            MiniConstructor(message.from_user.id, 'Для издания валюты требуется 10 Хостел-Коинов + 1 Хостел-Коин для издания хотя бы одной бумаги!', 'Эмиссия валюты!', 'Издать облигацию', 'Главное меню')
            return 1
        MenuConstructor(message.from_user.id, [0], CreateCurr, 'Издание валюты вам обойдется в 10 Хостел-Коинов + 1 Хостел-Коин за каждую бумагу.\n\nВведите название для вашей валюты', 'Главное меню')
        return 1

    elif message.text == 'Издать облигацию' and len(SqlCommit('SELECT * FROM users WHERE name = ?', (message.from_user.username,))) != 0:
        money = SqlCommit('SELECT Хостел_Коины FROM users WHERE name = ? ;', (message.from_user.username,))[0][0]
        if money > 10:
            MenuConstructor(message.from_user.id, [0], CreateContract, 'Облигация вам обойдется в 10 Хостел-Коинов + 1 Хостел-Коин за каждую бумагу.\n\nВведите название для вашей облигации', 'Главное меню')
            return 1
        MiniConstructor(message.from_user.id, 'Для издания облигации требуется 10 Хостел-Коинов + 1 Хостел-Коин для издания хотя бы одной бумаги!', 'Эмиссия валюты!', 'Издать облигацию', 'Главное меню')

    elif message.text == 'Настройки':
        keyboard = types.InlineKeyboardMarkup()
        url_button = types.InlineKeyboardButton(text='Написать разработчику', url='t.me/TerliPower')
        keyboard.add(url_button)
        msg = bot.send_message(message.from_user.id, 'Не потеряйтесь во всех этих кнопках! Вы можете написать разработчику, чтобы уведомить о багах или сделать предложение по боту', reply_markup = keyboard)

    elif message.text == 'Топ':
        MiniConstructor(message.from_user.id, GetTop('Хостел_Коины'), 'Мой аккаунт', 'Биржа', 'Банк', 'Топ', 'Настройки')

    elif message.text == 'Рассчитать' and message.from_user.username == 'TerliPower':
        MenuConstructor(message.from_user.id, [0], AdminAdd, 'Укажите валюту', *tuple(GetAllCurrencies()), 'Главное меню')

    elif message.text == 'Указать' and message.from_user.username == 'TerliPower':
        MenuConstructor(message.from_user.id, [0], AdminSet, 'Укажите ник', 'Главное меню')

    elif message.text == 'Анонс' and message.from_user.username == 'TerliPower':
        MenuConstructor(message.from_user.id, [0], SetAnnounce, 'Напишите анонс', 'Удалить', 'Главное меню')

    #elif message.text == 'd':
    #    MiniConstructor(message.from_user.id, 'hehe', *tuple(GetDatesMonth()))
    #    return 1

    elif len(SqlCommit('SELECT * FROM users WHERE name = ?', (message.from_user.username,))) != 0:
        if IsCurrExists(0, message.text) and message.text[0] == '📃':
            emitent = SqlCommit('SELECT emitent FROM bonds WHERE name = ? ;', (message.text,))[0][0]
            if emitent == message.from_user.username:
                MenuConstructor(message.from_user.id, [message.text], EditBond, GetCurrDescription(message.text), 'Задать описание', 'Главное меню')
            else:
                MiniConstructor(message.from_user.id, GetCurrDescription(message.text), 'Мой аккаунт', 'Биржа', 'Банк', 'Топ', 'Настройки')
            return 1
        MiniConstructor(message.from_user.id, 'Такой валюты нет! Кусь!', 'Перевести', 'Внести Ривалы', 'Вывести Ривалы', 'Главное меню')

bot.polling(none_stop=True, interval=0) #обязательная для работы бота часть
