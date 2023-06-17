import os
import time
import logging
from func import *
#from header import *

logging.basicConfig(level=logging.DEBUG, filename='BOTLOG',filemode='w')

def mainl():
    print('auto.py: mainl')
    try:
        print(GetSecondsToHour(18))
        time.sleep(GetSecondsToHour(18))
        while True:
            EachSixPm()
            time.sleep(86400)
    except KeyboardInterrupt:
        print('auto.py is closed')
    return 1

def EachSixPm():
    for curr in GetAllCurrencies():
        SqlCommit(f"UPDATE users SET {curr}_mean = ( ({curr} - {curr}_yes) + ({curr}_yes - {curr}_pyes) + ({curr}_pyes - {curr}_ppyes) ) / 3")
        SqlCommit(f"UPDATE users SET {curr}_ppyes = {curr}_pyes")
        SqlCommit(f"UPDATE users SET {curr}_pyes = {curr}_yes")
        SqlCommit(f"UPDATE users SET {curr}_yes = {curr}")
    today = datetime.today().date()
    for bond in GetAllBonds():
        print('bond is',bond)
        bond = SqlCommit(f"SELECT * FROM bonds WHERE name = '{bond}'")[0]
        print(bond)
        print(bond[6])
        if bond[6] == 1:
            continue
        dates = ListStrToDates(bond[7])
        for date in dates:
            print(date)
            if date == today:
                accs = SqlCommit(f"SELECT {bond[2]} FROM users WHERE {bond[2]} != 0")
                print(accs)
                i = -1
                for acc in accs:
                    print(acc)
                    i += 1
                    accs[i] = acc[0]
                ComAm = sum(accs)
                qmoney = ComAm * bond[5]
                money = SqlCommit(f"SELECT {bond[4]} FROM users WHERE tgid = %s", (bond[3],))[0][0]
                print(ComAm, qmoney, money)
                if qmoney > money:
                    print('qmon')
                    SqlCommit("UPDATE bonds SET isdef = 1 WHERE name = %s", (bond[2],))
                else:
                    print('tomath')
                    ToMatheAccount(bond[3], bond[4], -qmoney)
                    SqlCommit(f"UPDATE users SET {bond[4]} = {bond[2]} * {bond[5]} + {bond[4]} WHERE {bond[2]} != 0")  
    return 1

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
