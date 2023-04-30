import os
import time
from func import *
from header import *

def mainl():
    try:
        logging.debug(f'{GetSecondsToHour(18)}' + 'ii guys')
        logging.debug('bye guys')
        time.sleep(GetSecondsToHour(18))
        while True:
            EachSixPm()
            time.sleep(86400)
    except KeyboardInterrupt:
        print('auto.py is closed')
    return 1

def Iteration():
    a = '''SELECT * FROM bonds WHERE isdef = 0;'''
    cursor.execute(a)
    sqlite_connection.commit()
    bonds = cursor.fetchall()
    validbonds = []
    for bond in bonds:
        if ToMatheAccount(bond[3], bond[5], -bond[6] * bond[8]) == False:
            a = '''UPDATE bonds SET isdef = 1 WHERE name = ?;'''
            cursor.execute(a, (bond[2],))
            sqlite_connection.commit()
        else:
            validbonds.append(bond)
            print(bond)
    for bond in validbonds:
        SqlCommit(f'''UPDATE users SET {bond[5]} = {bond[6]} * {bond[2]} + {bond[5]};''')

def EachSixPm():
    for curr in GetAllCurrencies():
        SqlCommit(f'''UPDATE users SET {curr}_mean = ( ({curr} - {curr}_yes) + ({curr}_yes - {curr}_pyes) + ({curr}_pyes - {curr}_ppyes) ) / 3;''')
        SqlCommit(f'''UPDATE users SET {curr}_ppyes = {curr}_pyes;''')
        SqlCommit(f'''UPDATE users SET {curr}_pyes = {curr}_yes;''')
        SqlCommit(f'''UPDATE users SET {curr}_yes = {curr};''')
    today = datetime.today().date()
    for bond in GetAllBonds():
        bond = SqlCommit('SELECT * FROM bonds WHERE name = ?', (bond,))[0]
        print(bond[6])
        if bond[6] == 1:
            continue
        dates = ListStrToDates(bond[8])
        for date in dates:
            if date == today:
                accs = SqlCommit(f'SELECT {bond[2]} FROM users WHERE {bond[2]} != "None"')
                i = -1
                for acc in accs:
                    i += 1
                    accs[i] = acc[0]
                ComAm = sum(accs)
                qmoney = ComAm * bond[5]
                money = SqlCommit(f'SELECT {bond[4]} FROM users WHERE name = ?', (bond[3],))[0][0]
                print(ComAm, qmoney, money)
                if qmoney > money:
                    SqlCommit('UPDATE bonds SET isdef = 1 WHERE name = ?;', (bond[2],))
                else:
                    ToMatheAccount(bond[3], bond[4], -qmoney)
                    SqlCommit(f'UPDATE users SET {bond[4]} = {bond[2]} * {bond[5]} + {bond[4]} WHERE {bond[2]} != "None"')  
    return 1

mainl()
