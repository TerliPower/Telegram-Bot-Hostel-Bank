import os
import telebot
from telebot import types
from os.path import exists
from header import *

def TransmitMoney0(message):
    if IsCurrExists(curr = message.text):
        MenuConstructor(message.from_user.id, [message.text], TransmitMoney, f'Введите имя аккаунта телеграм, которому вы хотите перевести {message.text} (то, что идет после @)')
        return 1
    MiniConstructor(message.from_user.id, 'Такой валюты нет! Кусь!', 'Перевести', 'Внести Ривалы', 'Вывести Ривалы', 'Главное меню')

def TransmitMoney(message, curr):
    user = SqlCommit('''SELECT * FROM users WHERE name = ?;''', (message.text,))
    if len(user) != 0:
        MenuConstructor(message.from_user.id, [message.text, curr], TransmitMoney1, 'Введите сумму')
        return 1
    MiniConstructor(message.from_user.id, 'Такой игрок не зарегестрирован! Кусь!', 'Перевести', 'Внести Ривалы', 'Вывести Ривалы', 'Главное меню')

def IsValidForTransmit(userid, summa, add):
    if isinstance(add, int) == False:
        if add.isnumeric() == True:
            add = int(add)
        else:
            if userid != 0: MiniConstructor(userid, 'Введенные данные не корректны! Кусь!', 'Перевести', 'Внести Ривалы', 'Вывести Ривалы', 'Главное меню')
            return False
    if isinstance(summa, list) == True:
        print(summa, add)
        summa = summa[0][0]
    if isinstance(summa, str) == True:
        if summa.isnumeric() == True:
            summa = int(summa)
    if summa >= add:
        print('summa is ', summa, add)
        return True
    else:
        if userid != 0: MiniConstructor(userid, 'Такой суммы нет на вашем счете! Кусь!', 'Перевести', 'Внести Ривалы', 'Вывести Ривалы', 'Главное меню')
    return False

def TransmitMoney1(message, destname, currname):
    PATH_TO_ACCOUNT = f'users/{message.from_user.username}'
    add = message.text
    money = SqlCommit(f'''SELECT {currname} FROM users WHERE name = ?;''', (message.from_user.username,))
    if IsValidForTransmit(message.from_user.id, money, add):
        add = int(add)
        print('Money are trransmiting')
        SqlCommit(f'''UPDATE users SET {currname} = {currname} - {add} WHERE name = ?;''', (message.from_user.username,))
        SqlCommit(f'''UPDATE users SET {currname} = {currname} + {add} WHERE name = ?;''', (destname,))
        MiniConstructor(message.from_user.id, 'Ценные бумаги успешно переведены, ня', 'Перевести', 'Внести Ривалы', 'Вывести Ривалы', 'Главное меню')
        if currname[0] == '#':
            TransmitContracts(message.from_user.username, destname, currname, add)
    return 1

def ReplaceCurrKey(account, mark, key):
    key = str(key)
    with open(account, 'r') as file:
        data = file.readlines()
    i = -1
    for line in data:
        i = i + 1
        if line.strip():
            if line.split(' ', 1)[1].split(' ', 1)[0].find(mark) != -1:
                data[i] = ' ' + mark + ': ' + key + '\n'
    with open(account, 'w') as file:
        file.writelines(data)
    return 1

def RemoveHiddenMark(account, mark):
    with open(account, 'r') as file:
        data = file.readlines()
    with open(account, 'w') as file:
        i = -1
        for line in data:
            i = i + 1
            if line.find(' ' + mark + ' ') != False:
                file.write(line)
    return 1

def SetHiddenMark(account, mark, key):
    if key != 0:
        key = str(key)
        with open(account, 'a') as file:
            print(' ' + mark + ' ' + key + ' ', file = file)
    else:
        with open(account, 'a') as file:
            print(' ' + mark + ' ', file = file)
    return 1

def GetMarkKey(account, *mark):
    key = '-1'
    if len(mark) == 1:
        mark = str(mark[0])
        with open(account, 'r') as f:
            lines = f.readlines()
        for line in lines:
            if line.find(' ' + mark + ' ') != -1:
                key = line.split(" ")[2]
    else:
        mark = str(mark[0])
        with open(account, 'r') as f:
            lines = f.readlines()
        for line in lines:
            if line.find(' ' + mark + ': ') != -1:
                line = line[1:]
                key = line.split(' ')[1]
                key = key[:-1]
    return key

def GetCurrName(account, number):
    counter = 0
    with open(account, 'r') as f4:
        lines = f4.readlines()
        for line in lines:
            if line.find(':') != -1:
                counter += 1
                if counter == number:
                    name = line.split(" ")[1]
                    name = name[:-1]
                    return name
    return False

def IsThere(account, pattern):
    with open(account, 'r') as f5:
        lines = f5.readlines()
        for line in lines:
            if line.find(' ' + pattern + ' ') != -1:
                return True
    return False

def OrderHandler(message):
    PATH_TO_ACCOUNT = f'users/{message.from_user.username}'
    CommonAmount = GetMarkKey(PATH_TO_ACCOUNT, '💲Ривалы', 1)
    if IsValidForTransmit(message.from_user.id, GetMarkKey(PATH_TO_ACCOUNT, '💲Ривалы', 1), message.text):
        with open('OrdersPos', 'r') as f:
            number = f.read()[:-1]
        add = int(message.text)
        ToMathAccount(PATH_TO_ACCOUNT, '💲Ривалы', -add)
        with open('orders', 'a') as file:
            a = GetMarkKey(PATH_TO_ACCOUNT, "RRID")
            print(f'{number} {message.from_user.username} {a} {add}', file = file)
        with open('OrdersPos', 'w') as f:
            print(int(number) + 1, file = f)
        MiniConstructor(message.from_user.id, 'Заказ на вывод успешно создан, ожидайте, ня!', 'Главное меню')
    return 1    

def OrderHandler1(message):
    if message.text == 'Вывести':
        MenuConstructor(message.from_user.id, [0], OrderHandler, 'Введите желаемую к выводу сумму Ривалов и ожидайте их зачисления на свой аккаунт в Ривал Регионс. Вывод осуществляется вручную') 
    elif message.text == 'Снять заявку':
        MenuConstructor(message.from_user.id, [0], OrderHandler2, 'Выберите номер позиции')
        return 1
    return 1

def GetOrderData(pos):
    pos = str(pos)
    with open('orders', 'r') as file:
        data = file.readlines()
    for line in data:
        if line.split(' ',1)[0] == pos:
            owner = line.split(' ',1)[1].split(' ',1)[0]
            RRID = line.split(' ',1)[1].split(' ',1)[1].split(' ',1)[0]
            amount = line.split(' ',1)[1].split(' ',1)[1].split(' ',1)[1].split(' ',1)[0][:-1]
            print(owner, RRID, amount)
            return owner, RRID, amount
    return 0

def DeleteOrder(num):
    with open('orders', 'r') as file:
        data = file.readlines()
    with open('orders', 'w') as file:
        i = -1
        for line in data:
            i = i + 1
            if line.split(' ',1)[0] != num:
                file.write(line)
    return 1

def OrderHandler2(message):
    PATH_TO_ACCOUNT = f'users/{message.from_user.username}'
    if message.text.isnumeric() == False:
        MiniConstructor(message.from_user.id, 'Позиция должна быть числом!', 'Перевести', 'Внести Ривалы', 'Вывести Ривалы', 'Главное меню')
        return 0
    a = GetOrderData(message.text)
    if a == 0:
        MiniConstructor(message.from_user.id, 'Такой позиции у вас нет!', 'Перевести', 'Внести Ривалы', 'Вывести Ривалы', 'Главное меню')
        return 0
    print(a[0])
    if a[0] != message.from_user.username:
        MiniConstructor(message.from_user.id, 'Такой позиции у вас нет!', 'Перевести', 'Внести Ривалы', 'Вывести Ривалы', 'Главное меню')
        return 0
    ToMathAccount(PATH_TO_ACCOUNT, '💲Ривалы', a[2])
    DeleteOrder(message.text)
    MiniConstructor(message.from_user.id, 'Правильно правильно, все ривалы остануться здесь!', 'Перевести', 'Внести Ривалы', 'Вывести Ривалы', 'Главное меню')
    return 1

def IsCurrExists(curr):
    a = GetAllCurrencies()
    for currency_number in range(len(a)):
        if curr == a[currency_number]:
            return True
    return False

def ExchangeExhibit(message):
    PATH_TO_ACCOUNT = f'users/{message.from_user.username}'
    if IsCurrUserHas(message.from_user.username, message.text):
        MenuConstructor(message.from_user.id, [message.text], ExchangeExhibit1, f'Введите количество ценной бумаги {message.text}, которое вы хотите выставить', 'Главное меню')
        return 1
    MiniConstructor(message.from_user.id, 'Такой валюты у вас нет! Кусь!', 'Купить', 'Выставить', 'Главное меню')
    return 1

def ExchangeExhibit1(message, currname):
    PATH_TO_ACCOUNT = f'users/{message.from_user.username}'
    CommonAmount = int(GetMarkKey(PATH_TO_ACCOUNT, currname, 1))
    if IsValidForTransmit(message.from_user.id, CommonAmount, message.text):
        offeramount = int(message.text)
        MenuConstructor(message.from_user.id, [currname, offeramount], ExchangeExhibit2, 'Выберите ценную бумагу, которую вы хотите получить взамен', *tuple(GetAllExistCurr()), 'Главное меню')
    return 1

def ExchangeExhibit2(message, currname, offeramount):
    PATH_TO_ACCOUNT = f'users/{message.from_user.username}'
    a = GetAllExistCurr()
    if IsCurrExist(message.from_user.id, message.text):
        MenuConstructor(message.from_user.id, [currname, offeramount, message.text], ExchangeExhibit3, f'Введите количество ценной бумаги {message.text}, которое вы хотите получить за еденицу товара', 'Главное меню')
    return 1

def ExchangeExhibit3(message, currname, offeramount, querycurr):
    PATH_TO_ACCOUNT = f'users/{message.from_user.username}'
    queryam = message.text
    if queryam.isnumeric() == True:
        ToMathAccount(PATH_TO_ACCOUNT, currname, -offeramount)
        with open('ExchangePos', "r") as f:
                    ExchangePos = f.read()
        ExchangePos = ExchangePos[:-1]
        with open('exchange', 'a') as file:
            print(f'{ExchangePos}   {message.from_user.username}   {currname}: 1   {querycurr}: {queryam}   {offeramount}', file = file)
        ExchangePos = int(ExchangePos) + 1
        with open('ExchangePos', "w") as f:
            print(ExchangePos, file=f)
        MiniConstructor(message.from_user.id, 'Ценные бумаги успешно выставлены, ня', 'Мой аккаунт', 'Биржа', 'Банк', 'Топ', 'Настройки')
    else:
        MiniConstructor(message.from_user.id, 'Мда, что ты ввел вообще', 'Купить', 'Выставить', 'Главное меню')
    return 1

def ToMathAccount(account, currname, math):
    source = GetMarkKey(account, currname, 1)
    math = int(math)
    source = int(source)
    if math >= 0 or abs(math) <= source:
        if source != -1:
            source = int(source)
            ReplaceCurrKey(account, currname, source + math)
        else:
            SetCurr(account, currname, math)
        return 1
    return 0

def MenuConstructor(userid, listik, func, text, *buttons):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*buttons)
    msg = bot.send_message(userid, text, reply_markup = markup)
    if listik[0] == 0:
        bot.register_next_step_handler(msg, func)
    else:
        bot.register_next_step_handler(msg, func, *tuple(listik))
    return 1

def MiniConstructor(userid, text, *buttons):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*buttons)
    msg = bot.send_message(userid, text, reply_markup = markup)
    return 1

def CreateCurr(message):
    PATH_TO_ACCOUNT = f'users/{message.from_user.username}'
    a = GetAllForbCurr()
    if IsThereForbidSymbols(message.text):
        MiniConstructor(message.from_user.id, 'Использован зарезервированный символ! Не используйте специальные знаки и смайлики ✅ и 🤵', 'Эмиссия валюты!', 'Издать облигацию', 'Главное меню')
        return 1
    if IsCurrExist(0, message.text):
        MiniConstructor(message.from_user.id, 'Такая валюта уже есть!', 'Эмиссия валюты!', 'Издать облигацию', 'Главное меню')
        return 1
    MenuConstructor(message.from_user.id, [message.text], CreateCurr1, 'Какое количество валюты вы хотите выпустить?', 'Главное меню')
    return 1

def CreateCurr1(message, curr):
    PATH_TO_ACCOUNT = f'users/{message.from_user.username}'
    amount = message.text
    if amount.isnumeric() == True:
        SetCurr(PATH_TO_ACCOUNT, curr, amount)
        SetHiddenMark('currencies', curr, 0)
        SetInfo(PATH_TO_ACCOUNT, 'Эмитент', '\'' + curr + '\'')
        MiniConstructor(message.from_user.id, 'Поздравляю с выпуском новой валюты, ня', 'Эмиссия валюты!', 'Издать облигацию', 'Главное меню')
    else:
        MiniConstructor(message.from_user.id, 'Что ты ввел вообще мдаааа, попытайся снова', 'Эмиссия валюты!', 'Издать облигацию', 'Главное меню')
    return 1

def SetCurr(account, curr, amount):
    amount = str(amount)
    with open(account, "r") as f:
        contents = f.readlines()
    i = -1
    for line in contents:
        i += 1
        if line.find('///') != -1:
            break
    contents.insert(i, ' ' + curr + ': ' + amount + ' \n')
    with open(account, "w") as f:
        contents = "".join(contents)
        f.write(contents)
    return 1

def GetAllCurr(account):
    with open(account, "r") as f:
        contents = f.readlines()
    curr = []
    for line in contents:
        if line.find(': ') != -1:
            name = line.split(" ")[1]
            name = name[:-1]
            curr.append(name)
    return curr

def GetAllExistCurr():
    with open('currencies', "r") as f:
        contents = f.read()
    contents = contents.split('///',1)[1]
    contents = contents.splitlines()
    curr = []
    for line in contents:
        line = line[:-1]
        line = line[1:]
        curr.append(line)
    curr.pop(0)
    return curr

def ExchangeBuy(message):
    if GetPosData(message.text) != 0:
        pos = message.text
        MenuConstructor(message.from_user.id, [pos], ExchangeBuy1, 'Введите количество ценной бумаги, которое хотите купить', 'Главное меню')
    else:
        MiniConstructor(message.from_user.id, 'Такой позиции нет, кусь!', 'Купить', 'Выставить', 'Главное меню')
    return 1

def ExchangeBuy1(message, pos):
    PATH_TO_ACCOUNT = f'users/{message.from_user.username}'
    if message.text.isnumeric() == True:
        amount = int(message.text)
        a = GetPosData(pos)
        queryam = int(a[2])
        if amount <= queryam:
            c = GetMarkKey(PATH_TO_ACCOUNT, a[3], 1)
            c = int(c)
            b = amount * int(a[4])
            if c >= b:
                ToMathReserve(pos, -amount)
                ToMathAccount(PATH_TO_ACCOUNT, a[1], amount)
                ToMathAccount(PATH_TO_ACCOUNT, a[3], -(amount * int(a[4])))
                ToMathAccount(f'users/{a[0]}', a[3], amount * int(a[4]))
                MiniConstructor(message.from_user.id, 'Бумаги успешно приобретены, ня!', 'Купить', 'Выставить', 'Главное меню')
                counter = 0
                if a[1][0] == '#':
                    print('exc occur')
                    TransmitContracts(a[0] , message.from_user.username, a[1], amount)
                a = GetPosData(pos)
                if a[2] == ' 0':
                    DeletePos(pos)
            else:
                MiniConstructor(message.from_user.id, 'На вашем счету недостаточно средств для этого', 'Купить', 'Выставить', 'Главное меню')
        else:
            MiniConstructor(message.from_user.id, 'У данной позиции нет такого количества товара', 'Купить', 'Выставить', 'Главное меню')
    else:
        MiniConstructor(message.from_user.id, 'Что ты ввел ввобще мда', 'Купить', 'Выставить', 'Главное меню')
    return 1

def GetPosData(pos):
    pos = str(pos)
    with open('exchange', 'r') as file:
        data = file.readlines()
    for line in data:
        if line.split('   ',1)[0] == pos:
            owner = line.split('   ',1)[1].split('   ',1)[0]
            currec = line.split('   ',1)[1].split('   ',1)[1].split(' ',1)[0][:-1]
            cursend = line.split('   ',1)[1].split('   ',1)[1].split('   ',1)[1].split(' ',1)[0][:-1]
            cursendam = line.split('   ',1)[1].split('   ',1)[1].split('   ',1)[1].split(' ',1)[1].split('  ',1)[0]
            reserve = line.split('   ',1)[1].split('   ',1)[1].split('   ',1)[1].split(' ',1)[1].split('  ',1)[1][:-1]
            return owner, currec, reserve, cursend, cursendam
    return 0

def ToMathReserve(pos, math):
    with open('exchange', 'r') as file:
        data = file.readlines()
    i = -1
    for line in data:
        i = i + 1
        if line.split('   ',1)[0] == pos:
            linefrag = line.rsplit('   ',1)[0]
            reserve = line.rsplit('   ',1)[1]
            reserve = int(reserve)
            reserve = str(reserve + math)
            a = (linefrag, '   ', reserve, '\n')
            data[i] = ''.join(a)
    with open('exchange', 'w') as file:
        file.writelines(data)
    return 1

def DeletePos(pos):
    with open('exchange', 'r') as file:
        data = file.readlines()
    with open('exchange', 'w') as file:
        i = -1
        for line in data:
            i = i + 1
            if line.find(pos) != False:
                file.write(line)
    return 1

def CreateContract(message):
    PATH_TO_ACCOUNT = f'users/{message.from_user.username}'
    name = message.text
    a = GetAllForbCurr()
    if IsThereForbidSymbols(name):
        MiniConstructor(message.from_user.id, 'Использован зарезервированный символ! Не используйте специальные знаки и смайлик        и ✅ и 🤵', 'Эмиссия валюты!', 'Издать облигацию', 'Главное меню')
        return 1
    if IsCurrExist(0, message.text):
        MiniConstructor(message.from_user.id, 'Такая валюта уже есть или использовано зарезервированное слово или символ!',             'Эмиссия валюты!', 'Издать облигацию', 'Главное меню')
        return 1
    MenuConstructor(message.from_user.id, [name], CreateContract1, 'Укажите валюту выплаты купона', *tuple(GetAllCurrencies()), 'Главное меню')

def CreateContract1(message, name):
    curr = message.text
    a = GetAllExistCurr()
    c = -1
    if IsCurrExist(0, message.text):
        MenuConstructor(message.from_user.id, [name, curr], CreateContract2, 'Купон выплачивается каждые 10 минут, укажите сумму купона', 'Главное меню')
        return 1
    MiniConstructor(message.from_user.id, 'Такой валюты нет! Кусь!', 'Эмиссия валюты!', 'Издать облигацию', 'Главное меню') 

def CreateContract2(message, name, curr):
    value = message.text
    if value.isnumeric():
        MenuConstructor(message.from_user.id, [name, curr, value], CreateContract3, 'Укажите количество облигации, которое вы хотите выпустить', 'Главное меню')
        return 1
    MiniConstructor(message.from_user.id, 'Мда, что ты ввел вообще', 'Эмиссия валюты!', 'Издать облигацию', 'Главное меню')

def CreateContract3(message, name, curr, value):
    PATH_TO_ACCOUNT = f'users/{message.from_user.username}'
    amount = message.text
    if amount.isnumeric():
        a = '''INSERT INTO bonds(name, emitent, couponmin, couponcurr, couponprice, isdef) VALUES( ?, ?, ?, ?, ?, ? );'''
        cursor.execute(a, ('📃' + name, message.from_user.username, 10, curr, amount, False))
        sqlite_connection.commit()
        SqlCommit(f'''ALTER TABLE users ADD COLUMN {'📃' + name} INTEGER;''')
        SqlCommit(f'''UPDATE users SET {'📃' + name} = {amount} WHERE name = ?;''', (message.from_user.username,))
        MiniConstructor(message.from_user.id, 'Облигация успешно выпущена, ойеее', 'Главное меню')
        return 1
    MiniConstructor(message.from_user.id, 'Мда, что ты ввел вообще', 'Эмиссия валюты!', 'Издать облигацию', 'Главное меню')

def SetInfo(account, info, value):
    value = str(value)
    with open(account, "r") as f:
        contents = f.readlines()
    i = -1
    for line in contents:
        i += 1
        if line.find(':') != -1:
            break
    i -= 1
    contents.insert(i, ' ' + info + ' ' + value + ' \n')
    with open(account, "w") as f:
        contents = "".join(contents)
        f.write(contents)
    return 1

def EmisCurr(message, account, curr):
    amount = message.text
    if amount.isnumeric() == True:
        amount  = int(amount)
        ToMathAccount(account, curr, amount)
        MiniConstructor(message.from_user.id, 'Валюта успешно выпущена! Ура!', 'Мой аккаунт', 'Биржа', 'Банк', 'Топ', 'Настройки')
    else:
        MiniConstructor(message.from_user.id, 'Что ты ввел вообще мдаааа, попытайся снова', 'Мой аккаунт', 'Биржа', 'Банк', 'Топ', 'Настройки')
    return 1

def GetTop(curr):
    top = [0,0,0,0,0,0]
    topn = ['','','','','','']
    for filename in os.listdir('users'):
        if filename.endswith('~') == False and GetMarkKey(f'users/{filename}', 'Эмитент')[1:][:-1] != curr:
            raw = int(GetMarkKey(f'users/{filename}', curr, 1))
            if raw > top[5]:
                top[5] = raw

                topn[5] = filename
            if top[5] > top[4]:
                tmp = top[4]
                top[4] = top[5]
                top[5] = tmp

                tmpn = topn[4]
                topn[4] = topn[5]
                topn[5] = tmpn

            if top[4] > top[3]:
                tmp = top[3]
                top[3] = top[4]
                top[4] = tmp

                tmpn = topn[3]
                topn[3] = topn[4]
                topn[4] = tmpn

            if top[3] > top[2]:
                tmp = top[2]
                top[2] = top[3]
                top[3] = tmp

                tmpn = topn[2]
                topn[2] = topn[3]
                topn[3] = tmpn

            if top[2] > top[1]:
                tmp = top[1]
                top[1] = top[2]
                top[2] = tmp

                tmpn = topn[1]
                topn[1] = topn[2]
                topn[2] = tmpn
    i = 1
    text = '🤵Топ держателей Хостел-коина🏆\n\n\n🤵Держатель      🧾Количество\n\n'
    for i in range(6):
        if top[i] != 0:
            if i == 1:
                text += '🥇' + topn[i] + ':   ' + str(top[i]) + '📃\n'
            elif i == 2:
                text += '🥈' + topn[i] + ':   ' + str(top[i]) + '📃\n'
            elif i == 3:
                text += '🥉' + topn[i] + ':   ' + str(top[i]) + '📃\n'
            else:
                text += '🎉' + topn[i] + ':   ' + str(top[i]) + '📃\n'
    text = text[:-1]
    return text

def GetAllForbCurr():
    with open('currencies', "r") as f:
        contents = f.readlines()
    curr = []
    for line in contents:
        curr.append(line[1:][:-2])
    return curr

def IsThereForbidSymbols(text):
    special_characters = '✅🤵! @$%^&*()+?''""#_=,<>/'
    if any(c in special_characters for c in text):
        return 1
    return 0

def IsCurrExist(userid, curr):
    a = GetAllCurrencies()
    c = -1
    for i in a:
        c += 1
        if curr == a[c]:
            return True
    if userid != 0: MiniConstructor(userid, 'Такой валюты нет, кусь!', 'Купить', 'Выставить', 'Главное меню')
    return False

def AdminAdd(message):
    if IsCurrExist(message.text):
        MenuConstructor(message.from_user.id, [message.text], AdminAdd1, 'Укажите ник игрока')
        return 1
    MiniConstructor(message.from_user.id, 'Отдыхай')
    return 1

def AdminAdd1(message, curr):
    if exists(f'users/{message.text}'):
        MenuConstructor(message.from_user.id, [curr, message.text], AdminAdd2, 'Укажите сумму')
        return 1
    MiniConstructor(message.from_user.id, 'Отдыхай')
    return 1

def AdminAdd2(message, curr, dest):
    amount = message.text
    print(amount[0], amount[1:].isnumeric())
    if amount.isnumeric():
        amount = int(amount)
        ToMathAccount(f'users/{dest}', curr, amount)
        MiniConstructor(message.from_user.id, 'Успешно')
    elif amount[0] == '-' and amount[1:].isnumeric():
        amount = amount[1:]
        amount = int(amount)
        ToMathAccount(f'users/{dest}', curr, -amount)
        MiniConstructor(message.from_user.id, 'Успешно')
    else:
        MiniConstructor(message.from_user.id, 'Отдыхай')
    return 1

def StartDialog(userid, *args):

    if args[1]:
        print(args[0])
    else:
        print(args[2])

    return 1
#Dialog('Укажите ник игрока', &username)
#if IfExistCurr(msg) == False:
#   Dialog('Отдыхай', exit)
#   return 0
#Dialog('Укажите валюту', &curr)
#if IfExists(msg) == False:
#   Dialog('Отдыхай', exit)
#   return 0
#Dialog('Укажите сумму', &amount)
#if IsSumValid(msg) == False:
#   Dialog('Отдыхай', exit)
#   return 0
#TransmitMoney(username, curr, amount)
#Dialog('Успешно', exit)
#return 0

def AdminSet(message):
    if exists(f'users/{message.text}'):
        MenuConstructor(message.from_user.id, [message.text], AdminSet1, 'Укажите RRID')
        return 1
    MiniConstructor(message.from_user.id, 'Отдыхай')
    return 1

def AdminSet1(message, dest):
    RRID = message.text
    if RRID.isnumeric():
        SetInfo(f'users/{dest}', 'RRID', RRID)
        MiniConstructor(message.from_user.id, 'Успешно')
        return 1
    MiniConstructor(message.from_user.id, 'Отдыхай')
    return 1

def TransmitContracts(sender, receiver, contractname, amount):
    with open(f'curr/{contractname}', 'r') as f:
        senderacc = int(GetByNameAndNumber(f'curr/{contractname}', f'{sender}', 1))
        receiveracc = int(GetByNameAndNumber(f'curr/{contractname}', f'{receiver}', 1))
        RemoveMark(f'curr/{contractname}', f'{sender}')
        SetMark(f'curr/{contractname}', f'{sender}', str(senderacc - amount))
        if receiveracc == -1:
            SetMark(f'curr/{contractname}', f'{receiver}', amount)
        else:
            RemoveMark(f'curr/{contractname}', f'{receiver}')
            SetMark(f'curr/{contractname}', f'{receiver}', receiveracc + amount)

def GetByNameAndNumber(file, name, number):
    nline = '-1'
    with open(file, 'r') as f:
        lines = f.readlines()
    for line in lines:
        fname = line.split(' ', 1)[0]
        if name == fname:
            for i in range(number):
                line = line.split(' ', 1)[1]
            nline = line.split(' ', 1)[0]
    if nline[-1] == '\n':
        nline = nline[:-1]
    return nline

def RemoveMark(account, mark):
    with open(account, 'r') as file:
        data = file.readlines()
    with open(account, 'w') as file:
        i = -1
        for line in data:
            i = i + 1
            if line.find(mark + ' ') != False:
                file.write(line)
    return 1

def SetMark(account, mark, key):
    if key != 0:
        key = str(key)
        with open(account, 'a') as file:
            print(mark + ' ' + key, file = file)
    else:
        with open(account, 'a') as file:
            print(mark + ' ', file = file)
    return 1

def GetByNameAndNumber(file, name, number):
    nline = '-1'
    with open(file, 'r') as f:
        lines = f.readlines()
    for line in lines:
        fname = line.split(' ', 1)[0]
        if name == fname:
            for i in range(number):
                line = line.split(' ', 1)[1]
            nline = line.split(' ', 1)[0]
    if nline[-1] == '\n':
        nline = nline[:-1]
    return nline

def GetContractAccounts(name):
    with open(f'curr/{name}', "r") as f:
        contents = f.read()
    contents = contents.split('///',1)[1]
    contents = contents[1:]
    contents = contents.splitlines()
    curr = []
    for line in contents:
        name = line.split(' ', 1)[0]
        acc = line.split(' ', 1)[1]
        curr.append(name)
        curr.append(acc)
    return curr

def SetAnnounce(message):
    if message.text == 'Удалить':
        with open('announce', 'w') as f:
            print('', file =f)
    else:
        with open('announce', 'w') as f:
            print(message.text + '\n==============================================', file =f)
    MiniConstructor(message.from_user.id, 'Успешно', 'Главное меню')
    return 1

def ReturnPos(message):
    PATH_TO_ACCOUNT = f'users/{message.from_user.username}'
    if message.text.isnumeric() != True:
        MiniConstructor(message.from_user.id, 'Позиция должна быть числом', 'Главное меню')
        return 1
    a = GetPosData(int(message.text))
    print(a)
    if a == 0:
        MiniConstructor(message.from_user.id, 'Данной позиции не существует!', 'Главное меню')
        return 1
    if a[0] != message.from_user.username:
        MiniConstructor(message.from_user.id, 'Вы не владелец данной позиции!', 'Главное меню')
        return 1
    ToMathAccount(PATH_TO_ACCOUNT, a[1], a[2])
    DeletePos(message.text)
    MiniConstructor(message.from_user.id, 'Успешно снято!', 'Главное меню') # девочка с штукой с которой говорят "мотор"
    return 1

def SqlCommit(*args):
    cursor.execute(args[0], *args[1:])
    sqlite_connection.commit()
    return cursor.fetchall()

def GetAllCurrencies():
    cursor.execute('''PRAGMA table_info(users);''')
    sqlite_connection.commit()
    column_names = []
    for column in cursor.fetchall():
        column_names.append(column[1])
    for i in range(5):
        column_names.pop(0)
    return column_names
