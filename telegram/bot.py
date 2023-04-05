from header import *

@bot.message_handler(commands=['start'])
def start(message):
    PATH_TO_ACCOUNT = f'users/{message.from_user.username}'
    MenuConstructor(message.from_user.id, [0], get_text_messages, 'Привет, что вы хотите проверить?', 'Мой аккаунт', 'Биржа', 'Топ', 'Настройки')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    PATH_TO_ACCOUNT = f'users/{message.from_user.username}'
    if message.text == 'Мой аккаунт':
        if exists(PATH_TO_ACCOUNT) == False: #if account dont exists
            RRCode = randint(100000, 999999)
            with open(PATH_TO_ACCOUNT, "a") as f:
                print(f' 🤵{message.from_user.username}\n\n 💲Ривалы: 100\n 📃Хостел-коины: 100\n ///\n RRCode {RRCode}', file=f)
            with open(PATH_TO_ACCOUNT, "r") as f:
                text = f.read()
                text = text.split('///',1)[0]
            MenuConstructor(message.from_user.id, [0], get_text_messages, text, 'Перевести', 'Внести Ривалы', 'Вывести Ривалы', 'Главное меню')
        else:
            with open(PATH_TO_ACCOUNT, "r") as f:
                text = f.read()
                text = text.split('///',1)[0]
            MenuConstructor(message.from_user.id, [0], get_text_messages, text, 'Перевести', 'Внести Ривалы', 'Вывести Ривалы', 'Главное меню')

    elif message.text == 'Перевести' and exists(PATH_TO_ACCOUNT):
        MenuConstructor(message.from_user.id, [0], get_text_messages, 'Выберите ценную бумагу', *tuple(GetAllCurr(PATH_TO_ACCOUNT)), 'Главное меню')

    elif message.text == 'Главное меню':
        if exists(PATH_TO_ACCOUNT):
            MenuConstructor(message.from_user.id, [0], get_text_messages, 'Вы в главном меню, ня', 'Мой аккаунт', 'Биржа', 'Банк', 'Топ', 'Настройки')
        else:
            MenuConstructor(message.from_user.id, [0], get_text_messages, 'Вы в главном меню, ня', 'Мой аккаунт', 'Биржа', 'Топ', 'Настройки')

    elif message.text == 'Внести Ривалы' and exists(PATH_TO_ACCOUNT):
        if IsThere(PATH_TO_ACCOUNT, 'RRID') == False:
            MenuConstructor(message.from_user.id, [0], get_text_messages, f'Ваш аккаунт Телеграм не привязан к аккаунту Ривал Регионс. Верифицируйте ваш аккаунт, прислав ваш код верификации {GetMarkKey(PATH_TO_ACCOUNT,"RRCode")[:-1]} сообщением на аккаунт банка: https://m.rivalregions.com/#messages/246989401 и подождите принятия заявки, ня', 'Перевести', 'Внести Ривалы', 'Вывести Ривалы', 'Главное меню')
        else:
            MenuConstructor(message.from_user.id, [0], get_text_messages, 'Чтобы пополнить свой счет переведите желаемую сумму Ривалов на аккаунт банка: https://m.rivalregions.com/#slide/donate/user/246989401 и ожидайте поступления средств на ваш счет здесь (зачисления происходят вручную)', 'Перевести', 'Внести Ривалы', 'Вывести Ривалы', 'Главное меню')

    elif message.text == 'Вывести Ривалы' and exists(PATH_TO_ACCOUNT):
        if IsThere(PATH_TO_ACCOUNT, 'RRID') == False:
            MenuConstructor(message.from_user.id, [0], get_text_messages, f'Ваш аккаунт Телеграм не привязан к аккаунту Ривал Регионс. Верифицируйте ваш аккаунт, прислав ваш код верификации {GetMarkKey(PATH_TO_ACCOUNT,"RRCode")[:-1]} сообщением на аккаунт банка: https://m.rivalregions.com/#messages/246989401 и подождите принятия заявки, ня', 'Перевести', 'Внести Ривалы', 'Вывести Ривалы', 'Главное меню')
        else:
            MenuConstructor(message.from_user.id, [0], OrderHandler, 'Введите желаемую к выводу сумму Ривалов и ожидайте их зачисления на свой аккаунт в Ривал Регионс. Вывод осуществляется вручную')

    elif message.text == 'Биржа':
        if exists(PATH_TO_ACCOUNT):
            with open('exchange', "r") as f:
                    text = f.read()
            MenuConstructor(message.from_user.id, [0], get_text_messages, text, 'Купить', 'Выставить', 'Главное меню') 
        else:
            with open('exchange', "r") as f:
                    text = f.read()
            MenuConstructor(message.from_user.id, [0], get_text_messages, text, 'Главное меню')

    elif message.text == 'Выставить' and exists(PATH_TO_ACCOUNT):
        MenuConstructor(message.from_user.id, [0], ExchangeExhibit, 'Выберите ценную бумагу', *tuple(GetAllCurr(PATH_TO_ACCOUNT)), 'Главное меню')

    elif message.text == 'Купить' and exists(PATH_TO_ACCOUNT):
        MenuConstructor(message.from_user.id, [0], ExchangeBuy, 'Введите номер позиции, которую хотите купить', 'Главное меню')

    elif message.text == 'Банк' and exists(PATH_TO_ACCOUNT):
        MenuConstructor(message.from_user.id, [0], get_text_messages, 'Вы в банке, ня', 'Эмиссия валюты!', 'Издать облигацию', 'Главное меню')

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
        MenuConstructor(message.from_user.id, [0], get_text_messages, GetTop('📃Хостел-коины'), 'Мой аккаунт', 'Биржа', 'Банк', 'Топ', 'Настройки')

    elif message.text == 'Рассчитать' and message.from_user.username == 'TerliPower':
        MenuConstructor(message.from_user.id, [0], AdminAdd, 'Укажите валюту', *tuple(GetAllExistCurr()), 'Главное меню')

    elif message.text == 'Указать' and message.from_user.username == 'TerliPower':
        MenuConstructor(message.from_user.id, [0], AdminSet, 'Укажите ник', 'Главное меню')

    #elif message.text == 'd':
    #    print('do')
    #    DefaultHandler('test4', 4)

    elif exists(PATH_TO_ACCOUNT):
        for currency_number in range(len(GetAllCurr(PATH_TO_ACCOUNT))):
            if message.text == GetCurrName(PATH_TO_ACCOUNT, currency_number + 1):
                MenuConstructor(message.from_user.id, [message.text], NickCheck, f'Введите имя аккаунта телеграм, которому вы хотите перевести {message.text} (то, что идет после @)')

def NickCheck(message, curr):
    PATH_TO_ACCOUNT = f'users/{message.from_user.username}'
    if exists(f'users/{message.text}') == True: 
        MenuConstructor(message.from_user.id, [message.text, curr], TransmitMoney, 'Введите сумму')
    else:
        MenuConstructor(message.from_user.id, [0], get_text_messages, 'Такой игрок не зарегестрирован! Кусь!', 'Перевести', 'Внести Ривалы', 'Вывести Ривалы', 'Главное меню')

def TransmitMoney(message, destname, currname):
    PATH_TO_ACCOUNT = f'users/{message.from_user.username}'
    CommonAmount = GetMarkKey(PATH_TO_ACCOUNT, currname, 1)
    CommonAmount = int(CommonAmount)
    if message.text.isnumeric() == True:
        add = int(message.text)
        if CommonAmount >= add:
            ToMathAccount(PATH_TO_ACCOUNT, currname, -add)
            ToMathAccount(f'users/{destname}', currname, +add)
            MenuConstructor(message.from_user.id, [0], get_text_messages, 'Ценные бумаги успешно переведены, ня', 'Перевести', 'Внести Ривалы', 'Вывести Ривалы', 'Главное меню')
            if currname[0] == '#':
                TransmitContracts(message.from_user.username, destname, currname, add)
        else:
            MenuConstructor(message.from_user.id, [0], get_text_messages, 'Такой суммы нет на вашем счете! Кусь!', 'Перевести', 'Внести Ривалы', 'Вывести Ривалы', 'Главное меню')
    else:
        MenuConstructor(message.from_user.id, [0], get_text_messages, 'Введенные данные не корректны! Кусь!', 'Перевести', 'Внести Ривалы', 'Вывести Ривалы', 'Главно    е меню')
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
    key = 0
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
                print(line)
                line = line[1:]
                key = line.split(' ')[1]
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
    CommonAmount = GetMarkKey(PATH_TO_ACCOUNT, '💲Ривалы:')
    CommonAmount = int(CommonAmount)
    if message.text.isnumeric() == True:
        number = int(message.text)
        if CommonAmount < number:
            MenuConstructor(message.from_user.id, [0], get_text_messages, 'Такой суммы нет на вашем счете! Кусь!', 'Перевести', 'Внести Ривалы', 'Вывести Ривалы', 'Главное меню')
        else:
            ToMathAccount(PATH_TO_ACCOUNT, '💲Ривалы', -number)
            with open('orders', 'a') as file:
                a = GetMarkKey(PATH_TO_ACCOUNT, "RRID")
                a = a[:-1]
                print(f'{message.from_user.username} {a} {number}', file = file)
            MenuConstructor(message.from_user.id, [0], get_text_messages, 'Заказ на вывод успешно создан, ожидайте, ня!', 'Главное меню')
    else:
        MenuConstructor(message.from_user.id, [0], get_text_messages, 'Введенные данные не корректны! Кусь!', 'Перевести', 'Внести Ривалы', 'Вывести Ривалы', 'Главное меню') 
    return 1    

def ExchangeExhibit(message):
    PATH_TO_ACCOUNT = f'users/{message.from_user.username}'
    a = GetAllCurr(PATH_TO_ACCOUNT)
    for currency_number in range(len(a)):
        if message.text == a[currency_number]:
            MenuConstructor(message.from_user.id, [message.text], ExchangeExhibit1, f'Введите количество ценной бумаги {message.text}, которое вы хотите выставить', 'Главное меню')
            return 1
    MenuConstructor(message.from_user.id, [0], get_text_messages, 'Такой валюты у вас нет! Кусь!', 'Купить', 'Выставить', 'Главное меню')
    return 1

def ExchangeExhibit1(message, currname):
    PATH_TO_ACCOUNT = f'users/{message.from_user.username}'
    CommonAmount = GetMarkKey(PATH_TO_ACCOUNT, currname, 1)
    CommonAmount = int(CommonAmount)
    if message.text.isnumeric() == True:
        offeramount = int(message.text)
        if CommonAmount >= offeramount:
            MenuConstructor(message.from_user.id, [currname, offeramount], ExchangeExhibit2, 'Выберите ценную бумагу, которую вы хотите получить взамен', *tuple(GetAllExistCurr()), 'Главное меню')
        else:
            MenuConstructor(message.from_user.id, [0], get_text_messages, 'Такой суммы нет на вашем счете! Кусь!', 'Купить', 'Выставить', 'Главное меню')
    else:
        MenuConstructor(message.from_user.id, [0], get_text_messages, 'Введенные данные не корректны! Кусь!', 'Купить', 'Выставить', 'Главное меню')
    return 1

def ExchangeExhibit2(message, currname, offeramount):
    PATH_TO_ACCOUNT = f'users/{message.from_user.username}'
    a = GetAllExistCurr()
    for currency_number in range(len(a)):
        if message.text == a[currency_number]:
            MenuConstructor(message.from_user.id, [currname, offeramount, message.text], ExchangeExhibit3, f'Введите количество ценной бумаги {message.text}, которое вы хотите получить за еденицу товара', 'Главное меню')
            return 1
    MenuConstructor(message.from_user.id, [0], get_text_messages, 'Такой валюты нет, кусь!', 'Купить', 'Выставить', 'Главное меню')
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
        if currname[0] == '#':
            print('exc occur')
            TransmitContracts(message.from_user.username, 'ex', currname, offeramount)
        MenuConstructor(message.from_user.id, [0], get_text_messages, 'Ценные бумаги успешно выставлены, ня', 'Мой аккаунт', 'Биржа', 'Банк', 'Топ', 'Настройки')
    else:
        MenuConstructor(message.from_user.id, [0], get_text_messages, 'Мда, что ты ввел вообще', 'Купить', 'Выставить', 'Главное меню')
    return 1

def ToMathAccount(account, currname, math):
    if GetMarkKey(account, currname, 1) != 0:
        source = int(GetMarkKey(account, currname, 1))
        ReplaceCurrKey(account, currname, source + math)
    else:
        SetCurr(account, currname, math)
    return 1

def MenuConstructor(userid, listik, func, text, *buttons):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*buttons)
    msg = bot.send_message(userid, text, reply_markup = markup)
    if listik[0] == 0:
        bot.register_next_step_handler(msg, func)
    else:
        bot.register_next_step_handler(msg, func, *tuple(listik))
    return 1

def CreateCurr(message):
    PATH_TO_ACCOUNT = f'users/{message.from_user.username}'
    a = GetAllForbCurr()
    if IsThereForbidSymbols(message.text):
        MenuConstructor(message.from_user.id, [0], get_text_messages, 'Использован зарезервированный символ! Не используйте специальные знаки и смайлики ✅ и 🤵', 'Эмиссия валюты!', 'Издать облигацию', 'Главное меню')
        return 1
    for i in a:
        if message.text == i:
            MenuConstructor(message.from_user.id, [0], get_text_messages, 'Такая валюта уже есть или использовано зарезервированное слово или символ!', 'Эмиссия валюты!', 'Издать облигацию', 'Главное меню')
            return 1
    #with open('currencies', 'a') as file:
    #    print(message.text)
    MenuConstructor(message.from_user.id, [message.text], CreateCurr1, 'Какое количество валюты вы хотите выпустить?', 'Главное меню')
    return 1

def CreateCurr1(message, curr):
    PATH_TO_ACCOUNT = f'users/{message.from_user.username}'
    amount = message.text
    if amount.isnumeric() == True:
        SetCurr(PATH_TO_ACCOUNT, curr, amount)
        SetHiddenMark('currencies', curr, 0)
        SetInfo(PATH_TO_ACCOUNT, 'Эмитент', '\'' + curr + '\'')
        MenuConstructor(message.from_user.id, [0], get_text_messages, 'Поздравляю с выпуском новой валюты, ня', 'Эмиссия валюты!', 'Издать облигацию', 'Главное меню')
    else:
        MenuConstructor(message.from_user.id, [0], get_text_messages, 'Что ты ввел вообще мдаааа, попытайся снова', 'Эмиссия валюты!', 'Издать облигацию', 'Главное меню')
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
        MenuConstructor(message.from_user.id, [0], get_text_messages, 'Такой позиции нет, кусь!', 'Купить', 'Выставить', 'Главное меню')
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
                MenuConstructor(message.from_user.id, [0], get_text_messages, 'Бумаги успешно приобретены, ня!', 'Купить', 'Выставить', 'Главное меню')
                counter = 0
                if a[1][0] == '#':
                    print('exc occur')
                    TransmitContracts('ex', message.from_user.username, a[1], amount)
                a = GetPosData(pos)
                if a[2] == ' 0':
                    DeletePos(pos)
            else:
                MenuConstructor(message.from_user.id, [0], get_text_messages, 'На вашем счету недостаточно средств для этого', 'Купить', 'Выставить', 'Главное меню')
        else:
            MenuConstructor(message.from_user.id, [0], get_text_messages, 'У данной позиции нет такого количества товара', 'Купить', 'Выставить', 'Главное меню')
    else:
        MenuConstructor(message.from_user.id, [0], get_text_messages, 'Что ты ввел ввобще мда', 'Купить', 'Выставить', 'Главное меню')
    return 1

def GetPosData(pos):
    with open('exchange', 'r') as file:
        data = file.readlines()
    for line in data:
        if line.split('   ',1)[0].find(pos) != -1:
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
        MenuConstructor(message.from_user.id, [0], get_text_messages, 'Использован зарезервированный символ! Не используйте специальные знаки и смайлик        и ✅ и 🤵', 'Эмиссия валюты!', 'Издать облигацию', 'Главное меню')
        return 1
    for i in a:
        if message.text == i:
            MenuConstructor(message.from_user.id, [0], get_text_messages, 'Такая валюта уже есть или использовано зарезервированное слово или символ!',             'Эмиссия валюты!', 'Издать облигацию', 'Главное меню')
            return 1
    MenuConstructor(message.from_user.id, [name], CreateContract1, 'Укажите валюту выплаты купона', *tuple(GetAllCurr(PATH_TO_ACCOUNT)), 'Главное меню')

def CreateContract1(message, name):
    curr = message.text
    a = GetAllExistCurr()
    c = -1
    for i in a:
        c += 1
        if curr == a[c]:
            MenuConstructor(message.from_user.id, [name, curr], CreateContract2, 'Купон выплачивается каждые 10 минут, укажите сумму купона', 'Главное меню')
            return 1
    MenuConstructor(message.from_user.id, [0], get_text_messages, 'Такой валюты нет! Кусь!', 'Эмиссия валюты!', 'Издать облигацию', 'Главное меню') 

def CreateContract2(message, name, curr):
    value = message.text
    if value.isnumeric():
        MenuConstructor(message.from_user.id, [name, curr, value], CreateContract3, 'Укажите количество облигации, которое вы хотите выпустить', 'Главное меню')
        return 1
    MenuConstructor(message.from_user.id, [0], get_text_messages, 'Мда, что ты ввел вообще', 'Эмиссия валюты!', 'Издать облигацию', 'Главное меню')

def CreateContract3(message, name, curr, value):
    PATH_TO_ACCOUNT = f'users/{message.from_user.username}'
    amount = message.text
    if amount.isnumeric():
        MenuConstructor(message.from_user.id, [0], get_text_messages, 'Облигация успешно выпущена, ойеее', 'Главное меню')
        with open(f'curr/#{name}', 'w') as f:
            print(f'Ценная бумага: {name}', file = f)
            print(f'Эмитент: {message.from_user.username}', file = f)
            print(f'Общее количество: {amount}', file = f)
            print(f'Купон (каждые 10 минут): {curr}: {value}\n///', file = f)
            print(f'{message.from_user.username} {amount}', file = f)
        SetCurr(PATH_TO_ACCOUNT, '#' + name, amount)
        SetHiddenMark('currencies', f'#{name}', 0)
        return 1
    MenuConstructor(message.from_user.id, [0], get_text_messages, 'Мда, что ты ввел вообще', 'Эмиссия валюты!', 'Издать облигацию', 'Главное меню')

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
        MenuConstructor(message.from_user.id, [0], get_text_messages, 'Валюта успешно выпущена! Ура!', 'Мой аккаунт', 'Биржа', 'Банк', 'Топ', 'Настройки')
    else:
        MenuConstructor(message.from_user.id, [0], get_text_messages, 'Что ты ввел вообще мдаааа, попытайся снова', 'Мой аккаунт', 'Биржа', 'Банк', 'Топ', 'Настройки')
    return 1

def GetTop(curr):
    top = [0,0,0,0,0,0]
    topn = ['','','','','','']
    for filename in os.listdir('users'):
        if filename.endswith('~') == False:
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
    for i in range(5):
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

def AdminAdd(message):
    curr = message.text
    a = GetAllExistCurr()
    c = -1
    for i in a:
        c += 1
        if curr == a[c]:
            MenuConstructor(message.from_user.id, [curr], AdminAdd1, 'Укажите ник игрока')
            return 1
    MenuConstructor(message.from_user.id, [0], get_text_messages, 'Отдыхай')
    return 1

def AdminAdd1(message, curr):
    dest = message.text
    if exists(f'users/{dest}'):
        MenuConstructor(message.from_user.id, [curr, dest], AdminAdd2, 'Укажите сумму')
        return 1
    MenuConstructor(message.from_user.id, [0], get_text_messages, 'Отдыхай')
    return 1

def AdminAdd2(message, curr, dest):
    amount = message.text
    print(amount[0], amount[1:].isnumeric())
    if amount.isnumeric():
        amount = int(amount)
        ToMathAccount(f'users/{dest}', curr, amount)
        MenuConstructor(message.from_user.id, [0], get_text_messages, 'Успешно')
    elif amount[0] == '-' and amount[1:].isnumeric():
        amount = amount[1:]
        amount = int(amount)
        ToMathAccount(f'users/{dest}', curr, -amount)
        MenuConstructor(message.from_user.id, [0], get_text_messages, 'Успешно')
    else:
        MenuConstructor(message.from_user.id, [0], get_text_messages, 'Отдыхай')
    return 1

def AdminSet(message):
    dest = message.text
    if exists(f'users/{dest}'):
        MenuConstructor(message.from_user.id, [dest], AdminSet1, 'Укажите RRID')
        return 1
    MenuConstructor(message.from_user.id, [0], get_text_messages, 'Отдыхай')
    return 1

def AdminSet1(message, dest):
    PATH_TO_ACCOUNT = f'users/{message.from_user.username}'
    RRID = message.text
    if RRID.isnumeric():
        SetInfo(PATH_TO_ACCOUNT, 'RRID', RRID)
        MenuConstructor(message.from_user.id, [0], get_text_messages, 'Успешно')
        return 1
    MenuConstructor(message.from_user.id, [0], get_text_messages, 'Отдыхай')
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

bot.polling(none_stop=True, interval=0) #обязательная для работы бота часть