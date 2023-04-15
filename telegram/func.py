import os
import telebot
from telebot import types
from os.path import exists
from header import *

def TransmitMoney0(message):
    if IsCurrExists(0, message.text) == False:
        MiniConstructor(message.from_user.id, 'Такой валюты нет! Кусь!', 'Перевести', 'Внести Ривалы', 'Вывести Ривалы', 'Главное меню')
        return 1
    MenuConstructor(message.from_user.id, [message.text], TransmitMoney, f'Введите имя аккаунта телеграм, которому вы хотите перевести {message.text} (то, что идет после @)')
    print('bot.py: TransmitMoney0')
    return 1

def TransmitMoney(message, curr):
    user = SqlCommit('''SELECT * FROM users WHERE name = ?;''', (message.text,))
    if len(user) != 0:
        MenuConstructor(message.from_user.id, [message.text, curr], TransmitMoney1, 'Введите сумму')
        print('bot.py: TransmitMoney')
        return 1
    MiniConstructor(message.from_user.id, 'Такой игрок не зарегестрирован! Кусь!', 'Перевести', 'Внести Ривалы', 'Вывести Ривалы', 'Главное меню')

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

def TransmitMoney1(message, destname, currname):
    PATH_TO_ACCOUNT = f'users/{message.from_user.username}'
    add = message.text
    money = SqlCommit(f'''SELECT {currname} FROM users WHERE name = ?;''', (message.from_user.username,))
    if IsValidForTransmit(message.from_user.id, money, add, 'Перевести', 'Внести Ривалы', 'Вывести Ривалы', 'Главное меню'):
        add = int(add)
        print('Money are trransmiting')
        SqlCommit(f'''UPDATE users SET {currname} = {currname} - {add} WHERE name = ?;''', (message.from_user.username,))
        SqlCommit(f'''UPDATE users SET {currname} = {currname} + {add} WHERE name = ?;''', (destname,))
        MiniConstructor(message.from_user.id, 'Ценные бумаги успешно переведены, ня', 'Перевести', 'Внести Ривалы', 'Вывести Ривалы', 'Главное меню')
        print('bot.py: TransmitMoney1')
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
    CommonAmount = SqlCommit('SELECT ✅Ривалы FROM users WHERE name = ?', (message.from_user.username,))
    if IsValidForTransmit(message.from_user.id, CommonAmount, message.text, 'Мой аккаунт', 'Биржа', 'Банк', 'Топ', 'Настройки'):
        add = int(message.text)
        ToMatheAccount(message.from_user.username, '✅Ривалы', -add)
        RRID = SqlCommit('SELECT rrid FROM users WHERE name = ?', (message.from_user.username,))[0][0]
        SqlCommit('INSERT INTO orders(name, RRID, amount) VALUES(?, ?, ?)', (message.from_user.username, RRID, add))
        MiniConstructor(message.from_user.id, 'Заказ на вывод успешно создан, ожидайте, ня!', 'Главное меню')
        print('bot.py: OrderHandler')
    return 1    

def OrderHandler1(message):
    if message.text == 'Вывести':
        MenuConstructor(message.from_user.id, [0], OrderHandler, 'Введите желаемую к выводу сумму Ривалов и ожидайте их зачисления на свой аккаунт в Ривал Регионс. Вывод осуществляется вручную') 
    elif message.text == 'Снять заявку':
        MenuConstructor(message.from_user.id, [0], OrderHandler2, 'Выберите номер позиции')
    print('bot.py: OrderHandler1')
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
    if message.text.isnumeric() == False:
        MiniConstructor(message.from_user.id, 'Позиция должна быть числом!', 'Перевести', 'Внести Ривалы', 'Вывести Ривалы', 'Главное меню')
        return 0
    a = SqlCommit('SELECT * FROM orders WHERE id = ?', (message.text,))[0]
    if len(a) == 0:
        MiniConstructor(message.from_user.id, 'Такой позиции нет!', 'Перевести', 'Внести Ривалы', 'Вывести Ривалы', 'Главное меню')
        return 0
    if a[1] != message.from_user.username:
        MiniConstructor(message.from_user.id, 'Такой позиции у вас нет!', 'Перевести', 'Внести Ривалы', 'Вывести Ривалы', 'Главное меню')
        return 0
    ToMatheAccount(message.from_user.username, '✅Ривалы', a[3])
    SqlCommit('DELETE FROM orders WHERE id = ?', (message.text,))
    MiniConstructor(message.from_user.id, 'Правильно правильно, все ривалы остануться здесь!', 'Перевести', 'Внести Ривалы', 'Вывести Ривалы', 'Главное меню')
    print('bot.py: OrderHandler2')
    return 1

def IsCurrExists(userid, curr):
    a = GetAllCurrencies()
    for currency_number in range(len(a)):
        if curr == a[currency_number]:
            return True
    if userid != 0: MiniConstructor(userid, 'Такой валюты нет, кусь!', 'Купить', 'Выставить', 'Главное меню')
    return False

def ExchangeExhibit(message):
    if IsCurrUserHas(message.from_user.username, message.text):
        MenuConstructor(message.from_user.id, [message.text], ExchangeExhibit1, f'Введите количество ценной бумаги {message.text}, которое вы хотите выставить', 'Главное меню')
        print('bot.py: ExchangeExhibit')
        return 1
    MiniConstructor(message.from_user.id, 'Такой валюты у вас нет! Кусь!', 'Купить', 'Выставить', 'Главное меню')
    return 1

def ExchangeExhibit1(message, currname):
    CommonAmount = SqlCommit(f'SELECT {currname} FROM users WHERE name = ?', (message.from_user.username,))[0][0]
    if IsValidForTransmit(message.from_user.id, CommonAmount, message.text, 'Купить', 'Выставить', 'Главное меню'):
        offeramount = int(message.text)
        MenuConstructor(message.from_user.id, [currname, offeramount], ExchangeExhibit2, 'Выберите ценную бумагу, которую вы хотите получить взамен', *tuple(GetAllCurrencies()), 'Главное меню')
        print('bot.py: ExchangeExhibit1')
    return 1

def ExchangeExhibit2(message, currname, offeramount):
    PATH_TO_ACCOUNT = f'users/{message.from_user.username}'
    if IsCurrExists(message.from_user.id, message.text):
        MenuConstructor(message.from_user.id, [currname, offeramount, message.text], ExchangeExhibit3, f'Введите количество ценной бумаги {message.text}, которое вы хотите получить за еденицу товара', 'Главное меню')
        print('bot.py: ExchangeExhibit2')
    return 1

def ExchangeExhibit3(message, currname, offeramount, querycurr):
    queryam = message.text
    if queryam.isnumeric() != True:
        MiniConstructor(message.from_user.id, 'Мда, что ты ввел вообще', 'Купить', 'Выставить', 'Главное меню')
        return 1
    ToMatheAccount(message.from_user.username, currname, -offeramount)
    SqlCommit(f'INSERT INTO exchange(name, get, send, amount, reserve) VALUES(?, ?, ?, ?, ?)', (message.from_user.username, currname, querycurr, queryam, offeramount))
    MiniConstructor(message.from_user.id, 'Ценные бумаги успешно выставлены, ня', 'Мой аккаунт', 'Биржа', 'Банк', 'Топ', 'Настройки')
    print('bot.py: ExchangeExhibit3')
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
    if IsThereForbidSymbols(message.text):
        MiniConstructor(message.from_user.id, 'Использован зарезервированный символ! Не используйте специальные знаки и смайлики ✅ и 🤵', 'Эмиссия валюты!', 'Издать облигацию', 'Главное меню')
        return 1
    if IsTextHasEmoji(message.text):
        MiniConstructor(message.from_user.id, 'Смайлики запрещены!', 'Эмиссия валюты!', 'Издать облигацию', 'Главное меню')
        return 1
    if IsCurrExists(0, message.text):
        MiniConstructor(message.from_user.id, 'Такая валюта уже существует!', 'Эмиссия валюты!', 'Издать облигацию', 'Главное меню')
        return 1
    money = SqlCommit('SELECT Хостел_Коины FROM users WHERE name = ?;', (message.from_user.username,))[0][0] - 10
    MenuConstructor(message.from_user.id, [message.text], CreateCurr1, f'Введите желаемое количество валюты для выпуска\n\nОдна бумага обойдется вам в 1 Хостел-Коин. Вы можете выпустить {money} бумаг', 'Главное меню')
    print('bot.py: CreateCurr')
    return 1

def CreateCurr1(message, curr):
    if message.text.isnumeric() != True:
        MiniConstructor(message.from_user.id, 'Мда, что ты ввел вообще', 'Эмиссия валюты!', 'Издать облигацию', 'Главное меню')
        print(1)
        return 1
    money = SqlCommit('SELECT Хостел_Коины FROM users WHERE name = ?;', (message.from_user.username,))[0][0]
    amount = int(message.text)
    if money < 10 + amount:
        print(2)
        MiniConstructor(message.from_user.id, 'Вам не хватает Хостел-Коинов', 'Эмиссия валюты!', 'Издать облигацию', 'Главное меню')
        return 1
    SqlCommit(f'UPDATE users SET emitent = ? WHERE name = ?;', (curr, message.from_user.username,))
    SqlCommit(f'ALTER TABLE users ADD {curr} INTEGER;', '')
    SqlCommit(f'ALTER TABLE users ADD {curr}_yes INTEGER;', '')
    SqlCommit(f'ALTER TABLE users ADD {curr}_pyes INTEGER;', '')
    SqlCommit(f'ALTER TABLE users ADD {curr}_ppyes INTEGER;', '')
    SqlCommit(f'ALTER TABLE users ADD {curr}_mean INTEGER;', '')
    SqlCommit(f'UPDATE users SET {curr}_mean = 0;')
    SqlCommit(f'UPDATE users SET {curr} = {amount} WHERE name = ?;', (message.from_user.username,))
    SqlCommit(f'UPDATE users SET {curr} = {amount} WHERE name = ?;', (message.from_user.username,))
    SqlCommit(f'''UPDATE users SET Хостел_Коины = Хостел_Коины - 10 - {amount} WHERE name = ?;''', (message.from_user.username,))
    MiniConstructor(message.from_user.id, 'Поздравляю с выпуском новой валюты, ня', 'Эмиссия валюты!', 'Издать облигацию', 'Главное меню')
    print('bot.py: CreateCurr1')
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
    if len(SqlCommit('SELECT id FROM exchange WHERE id = ?', (message.text,))) == 0:
        MiniConstructor(message.from_user.id, 'Такой позиции нет, кусь!', 'Купить', 'Выставить', 'Главное меню')
        return 1
    MenuConstructor(message.from_user.id, [message.text], ExchangeBuy1, 'Введите количество ценной бумаги, которое хотите купить', 'Главное меню')
    print('bot.py: ExchangeBuy')
    return 1

def ExchangeBuy1(message, pos):
    if message.text.isnumeric() != True:
        MiniConstructor(message.from_user.id, 'Что ты ввел ввобще мда', 'Купить', 'Выставить', 'Главное меню')
        return 1
    qamount = int(message.text)
    pos = SqlCommit('SELECT * FROM exchange WHERE id = ?', (pos,))[0]
    print(pos)
    reserve = pos[5]
    if qamount > pos[5]:
        MiniConstructor(message.from_user.id, 'У данной позиции нет такого количества товара', 'Купить', 'Выставить', 'Главное меню')
        return 1
    money = SqlCommit(f'SELECT {pos[3]} FROM users WHERE name = ?', (message.from_user.username,))[0][0]
    rmoney = qamount * pos[4]
    if rmoney > money:
        MiniConstructor(message.from_user.id, 'На вашем счету недостаточно средств для этого', 'Купить', 'Выставить', 'Главное меню')
        return 1
    SqlCommit(f'UPDATE exchange SET reserve = reserve - {qamount} WHERE id = ?', (pos[0],))
    ToMatheAccount(message.from_user.username, pos[2], qamount)
    price = qamount * pos[4]
    ToMatheAccount(message.from_user.username, pos[3], -price)
    ToMatheAccount(pos[1], pos[3], price)
    MiniConstructor(message.from_user.id, 'Бумаги успешно приобретены, ня!', 'Купить', 'Выставить', 'Главное меню')
    SqlCommit('DELETE FROM exchange WHERE reserve = 0')
    print('bot.py: ExchangeBuy1')
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
        MiniConstructor(message.from_user.id, 'Не используйте специальные знаки!', 'Эмиссия валюты!', 'Издать облигацию', 'Главное меню')
        return 1
    if IsTextHasEmoji(message.text):
        MiniConstructor(message.from_user.id, 'Смайлики запрещены!', 'Эмиссия валюты!', 'Издать облигацию', 'Главное меню')
        return 1
    if IsCurrExist(0, '📃' + message.text):
        MiniConstructor(message.from_user.id, 'Такая бумага уже есть или использовано зарезервированное слово или символ!',             'Эмиссия валюты!', 'Издать облигацию', 'Главное меню')
        return 1
    listik = []
    MenuConstructor(message.from_user.id, [name, listik], CreateContract01, 'Укажите даты выплаты купона', *tuple(GetDatesMonth()), 'Главное меню')
    print('bot.py: CreateContract')

def CreateContract01(message, name, listik):
    if message.text == 'Закончить' and len(listik) != 0:
        MenuConstructor(message.from_user.id, [name, listik], CreateContract1, 'Укажите валюту выплаты купона', *tuple(GetAllCurrencies()), 'Главное меню')
        return 1
    if message.text == 'Закончить' and len(listik) == 0:
        MenuConstructor(message.from_user.id, [name, listik], CreateContract01, 'Выберите хотя бы одну дату!', *tuple(GetDatesMonth()),     'Главное меню')
        return 1
    if IsDate(message.text) != True:
        MiniConstructor(message.from_user.id, 'Что ты написал мдааа', 'Эмиссия валюты!', 'Издать облигацию', 'Главное меню') 
        return 1
    date = datetime.strptime(message.text, '%d %B %Y').date()
    today = datetime.today().date()
    monthlater = (datetime.today().date() + timedelta(days = 30))
    if today > date or date >= monthlater:
        MiniConstructor(message.from_user.id, 'Дата должна быть в пределах месяца', 'Эмиссия валюты!', 'Издать облигацию', 'Главное меню') 
        return 1
    listik.append(date)
    MenuConstructor(message.from_user.id, [name, listik], CreateContract01, 'Укажите следующую дату или закончте имеющимися', 'Закончить', *tuple(GetDatesMonth()), 'Главное меню')
    print('bot.py: CreateContract01')

def CreateContract1(message, name, listik):
    a = GetAllExistCurr()
    c = -1
    if IsCurrExist(0, message.text) != True:
        MiniConstructor(message.from_user.id, 'Такой валюты нет! Кусь!', 'Эмиссия валюты!', 'Издать облигацию', 'Главное меню') 
        return 1
    profit = SqlCommit(f'SELECT {message.text}_mean FROM users WHERE name = ?;', (message.from_user.username,))[0][0]
    daystolastcoup = (max(listik) - datetime.today().date()).days
    cprofit = (profit * daystolastcoup) / len(listik)
    MenuConstructor(message.from_user.id, [name, listik, message.text, cprofit], CreateContract2, f'Укажите сумму 1 купона\n\nСумма купона ограничена по формуле: ваш средний ежедневный доход по валюте ({message.text}: {profit}/в день) * дни до выплаты последнего купона ({daystolastcoup} дней) / количество купонов ({len(listik)}) и равно: {cprofit}', 'Главное меню')
    print('bot.py: CreateContract1')
    return 1

def CreateContract2(message, name, listik, curr, cprofit):
    if message.text.isnumeric() != True:
        MiniConstructor(message.from_user.id, 'Мда, что ты ввел вообще', 'Эмиссия валюты!', 'Издать облигацию', 'Главное меню')
        return 1
    if int(message.text) > cprofit:
        MiniConstructor(message.from_user.id, f'Ваша сумма купона не может превышать {cprofit}', 'Главное меню')
        return 1
    money = SqlCommit('SELECT Хостел_Коины FROM users WHERE name = ?;', (message.from_user.username,))[0][0] - 10
    MenuConstructor(message.from_user.id, [name, listik, curr, message.text], CreateContract3, f'Укажите количество облигации, которое вы хотите выпустить, одна бумага обойдется вам в 1 Хостел-Коин. Вы можете издать {money} облигаций', 'Главное меню')
    print('bot.py: CreateContract2')
    return 1

def CreateContract3(message, name, listik, curr, value):
    if message.text.isnumeric() != True:
        MiniConstructor(message.from_user.id, 'Мда, что ты ввел вообще', 'Эмиссия валюты!', 'Издать облигацию', 'Главное меню')
        return 1
    money = SqlCommit('SELECT Хостел_Коины FROM users WHERE name = ?;', (message.from_user.username,))[0][0]
    amount = int(message.text)
    if money < 10 + amount:
        MiniConstructor(message.from_user.id, 'Вам не хватает Хостел-Коинов', 'Эмиссия валюты!', 'Издать облигацию', 'Главное меню')
        return 1
    listik = DatesToStr(listik)
    name = '📃' + name
    a = '''INSERT INTO bonds(name, emitent, couponcurr, couponprice, isdef, commonamount, dates) VALUES( ?, ?, ?, ?, ?, ?, ?);'''
    cursor.execute(a, (name, message.from_user.username, curr, value, False, amount, listik))
    sqlite_connection.commit()
    SqlCommit(f'''ALTER TABLE users ADD COLUMN {name} INTEGER;''')
    SqlCommit(f'ALTER TABLE users ADD {name}_yes INTEGER;', '')
    SqlCommit(f'ALTER TABLE users ADD {name}_pyes INTEGER;', '')
    SqlCommit(f'ALTER TABLE users ADD {name}_ppyes INTEGER;', '')
    SqlCommit(f'ALTER TABLE users ADD {name}_mean INTEGER;', '')
    SqlCommit(f'UPDATE users SET {name}_mean = 0;')
    SqlCommit(f'''UPDATE users SET {name} = {amount} WHERE name = ?;''', (message.from_user.username,))
    SqlCommit(f'''UPDATE users SET Хостел_Коины = Хостел_Коины - 10 - {amount} WHERE name = ?;''', (message.from_user.username,))
    MiniConstructor(message.from_user.id, 'Облигация успешно выпущена, ойеее', 'Главное меню')
    print('bot.py: CreateContract3')
    return 1

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
    if message.text.isnumeric() == False:
        MiniConstructor(message.from_user.id, 'Что ты ввел вообще мдаааа, попытайся снова', 'Мой аккаунт', 'Биржа', 'Банк', 'Топ', 'Настройки')
        return 1
    am = int(message.text)
    ToMatheAccount(account, 'Хостел_Коины', -am)
    ToMatheAccount(account, curr, am)
    MiniConstructor(message.from_user.id, 'Валюта успешно выпущена! Ура!', 'Мой аккаунт', 'Биржа', 'Банк', 'Топ', 'Настройки')
    print('bot.py: EmisCurr')

def GetTop(curr):
    top = [0,0,0,0,0,0]
    topn = ['','','','','','']
    accs = SqlCommit(f'SELECT name,{curr} FROM users WHERE {curr} != "None AND emitent != {curr}"')
    for acc in accs:
        if acc[1] > top[5]:
            top[5] = acc[1]

            topn[5] = acc[0]
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
    print('bot.py: GetTop')
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
    if IsCurrExists(0, message.text):
        MenuConstructor(message.from_user.id, [message.text], AdminAdd1, 'Укажите ник игрока')
        return 1
    MiniConstructor(message.from_user.id, 'Отдыхай')
    return 1

def AdminAdd1(message, curr):
    if len(SqlCommit('SELECT * FROM users WHERE name = ?', (message.text,))) != 0:
        MenuConstructor(message.from_user.id, [curr, message.text], AdminAdd2, 'Укажите сумму')
        return 1
    MiniConstructor(message.from_user.id, 'Отдыхай')
    return 1

def AdminAdd2(message, curr, dest):
    if message.text.isnumeric():
        amount = int(message.text)
        ToMatheAccount(dest, curr, amount)
        MiniConstructor(message.from_user.id, 'Успешно')
    elif message.text[0] == '-' and message.text[1:].isnumeric():
        amount = int(message.text[1:])
        ToMatheAccount(dest, curr, -amount)
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
    if len(SqlCommit('SELECT * FROM users WHERE name = ?', (message.text,))) != 0:
        MenuConstructor(message.from_user.id, [message.text], AdminSet1, 'Укажите RRID')
        return 1
    MiniConstructor(message.from_user.id, 'Отдыхай')
    return 1

def AdminSet1(message, dest):
    RRID = message.text
    if RRID.isnumeric():
        SqlCommit(f'UPDATE users SET rrid = {RRID} WHERE name = ?', (dest,))
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
    if message.text.isnumeric() != True:
        MiniConstructor(message.from_user.id, 'Позиция должна быть числом', 'Главное меню')
        return 1
    pos = SqlCommit('SELECT * FROM exchange WHERE id = ?', (message.text,))
    if len(pos) == 0:
        MiniConstructor(message.from_user.id, 'Данной позиции не существует!', 'Главное меню')
        return 1
    pos = pos[0]
    if pos[1] != message.from_user.username:
        MiniConstructor(message.from_user.id, 'Вы не владелец данной позиции!', 'Главное меню')
        return 1
    ToMatheAccount(message.from_user.username, pos[2], pos[5])
    SqlCommit('DELETE FROM exchange WHERE id = ?', (pos[0],))
    MiniConstructor(message.from_user.id, 'Успешно снято!', 'Главное меню') # девочка с штукой с которой говорят "мотор"
    print('bot.py: ReturnPos')
    return 1

def SqlCommit(*args):
    cursor.execute(args[0], *args[1:])
    sqlite_connection.commit()
    return cursor.fetchall()

def GetAllCurrencies():
    cursor.execute('''PRAGMA table_info(users);''')
    sqlite_connection.commit()
    column_names = []
    for columninfo in cursor.fetchall():
        column_names.append(columninfo[1])
    for i in range(5):
        column_names.pop(0)
    column_names1 = []
    for i in range(0, len(column_names), 5):
        column_names1.append(column_names[i])
    print(column_names1)
    return column_names1

def ToMatheAccount(name, curr, value):
    money = SqlCommit(f'''SELECT {curr} FROM users WHERE name = ?;''', (name,))
    if IsValidForTransmit(0, money, value) or value > 0:
        value = int(value)
        isnone = SqlCommit(f'SELECT {curr} FROM users WHERE name = ?', (name,))[0][0]
        if isnone == None:
            SqlCommit(f'''UPDATE users SET {curr} = {value} WHERE name = ?;''', (name,))
            print('exc work')
        else:
            SqlCommit(f'''UPDATE users SET {curr} = {curr} + ({value}) WHERE name = ?;''', (name,))
        return True
    return False

def GetCurrDescription(curr):
    data = SqlCommit('''SELECT * FROM bonds WHERE name = ?;''', (curr,))
    data = data[0]
    if data[1] == None:
        des = 'Описание облигации не задано\n'
    else: des = data[1] + '\n'
    if data[7] == 1:
        des1 = 'По облигации обьявлен дефолт! Она больше не выплачивается!'
    else: des1 = ''
    print(data)
    data = des1 + '\nНазвание облигации: ' + data[2] + '\n' + 'Описание: ' + des + 'Эмитент: ' + data[3] + '\nДаты выплаты купона: ' + data[8] + '\nОбщее количество: ' + str(data[7])
    print('bot.py: GetCurrDescription')
    return data

def EditBond(message, bondname):
    if message.text == 'Задать описание':
        MenuConstructor(message.from_user.id, [bondname], EditBond1, 'Введите описание для вашей облигации', 'Главное меню')
        return 1
    MiniConstructor(message.from_user.id, 'Вы в главном меню', 'Мой аккаунт', 'Биржа', 'Банк', 'Топ', 'Настройки')
    print('bot.py: EditBond')

def EditBond1(message, bondname):
    SqlCommit(f'''UPDATE bonds SET description = ? WHERE name = ?;''', (message.text, bondname))
    MiniConstructor(message.from_user.id, GetCurrDescription(bondname), 'Мой аккаунт', 'Биржа', 'Банк', 'Топ', 'Настройки')
    print('bot.py: EditBond1')
    return 1

def IsTextHasEmoji(text):
    for character in text:
        if character in emoji.EMOJI_DATA:
            return True
    return False

def GetDatesMonth():
    dates = []
    for data in pd.date_range(start = datetime.now().date(), periods = 30, inclusive = 'right').to_pydatetime().tolist():
        dates.append(data.strftime('%d %B %Y'))
    return dates

def IsDate(date):
    try:
        datetime.strptime(date, '%d %B %Y')
        return True
    except ValueError:
        return False

def ListStrToDates(string):
    am = string.count(', ')
    listik = string.split(', ', am)
    i = -1
    for date in listik:
        i += 1
        listik[i] = datetime.strptime(date, '%Y-%m-%d').date()
    return listik

def DatesToStr(listik):
    i = -1
    for date in listik:
        i += 1
        listik[i] = str(date)
    listik = ', '.join(listik)
    return listik

def GetAllBonds():
    currs = GetAllCurrencies()
    bonds = []
    for curr in currs:
        if curr[0] == '📃':
            bonds.append(curr)
    return bonds

def GetSecondsToHour(hour):
    begin = datetime.combine(date.min, dt.datetime.now().time())
    end = datetime.combine(date.min, dt.time(hour = hour))
    duration = end - begin
    if begin > end:
        duration = duration + timedelta(days = 1)
    duration = duration.total_seconds()
    return duration

def GetAllCurrsUserHas(name):
    currs = []
    for curr in GetAllCurrencies():
        number = str(SqlCommit(f'SELECT {curr} FROM users WHERE name = ?;', (name,))[0][0])
        if number == 'None':
            continue
        currs.append(curr)
    return currs

def IsCurrUserHas(name, qcurr):
    currs = GetAllCurrsUserHas(name)
    for curr in currs:
        if curr == qcurr:
            return True
    return False
