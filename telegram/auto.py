import os
import time

def mainl():
    try:
        while True:
            Iteration()
            time.sleep(5)
    except KeyboardInterrupt:
        print('auto.py is closed')
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

def GetMarkKey(account, *mark):
    key = -1
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
    return key

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

def Iteration():
    for filename in os.listdir('curr'):
        if filename[0] == '#':
            if GetByNameAndNumber(f'curr/{filename}', 'Обьявлен', 1) == '-1':
                emitent = GetByNameAndNumber(f'curr/{filename}', 'Эмитент:', 1)
                curr = GetByNameAndNumber(f'curr/{filename}', 'Купон', 4)[:-1]
                value = int(GetByNameAndNumber(f'curr/{filename}', 'Купон', 5))
                amount = int(GetByNameAndNumber(f'curr/{filename}', 'Общее', 2))
                if ToMathAccount(f'users/{emitent}', curr, -value*amount) == 0:
                    with open(f'curr/{filename}', 'r') as f:
                        content = f.read()
                    with open(f'curr/{filename}', 'w') as f:
                        print('Обьявлен дефолт! Бумага не выплачивается!\n' + content[:-1], file = f)
                else:
                    a = GetContractAccounts(filename)
                    num = len(a)
                    for i in range(0, num, 2):
                        ToMathAccount(f'users/{a[i]}', curr, value*int(a[i+1])) 
            else:
                print('Обьявлен дефолт!')

mainl()

def TransmitContracts(sender, receiver, contractname, amount):
    with open(f'curr/{contractname}', 'r') as f:
        senderacc = int(GetByNameAndNumber(f'curr/{contractname}', f'{sender}', 1))
        receiveracc = int(GetByNameAndNumber(f'curr/{contractname}', f'{receiver}', 1))
        
        RemoveMark(f'curr/{contractname}', f'{sender}')
        SetMark(f'curr/{contractname}', f'{sender}', senderacc - amount)

        if receiveracc == -1:
            SetMark(f'curr/{contractname}', f'{receiver}', amount)
        else: 
            RemoveMark(f'curr/{contractname}', f'{receiver}')
            SetMark(f'curr/{contractname}', f'{receiver}', receiveracc + amount)

























