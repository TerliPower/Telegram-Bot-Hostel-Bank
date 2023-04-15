from glob import glob
from random import randint
from telebot import types
from os.path import exists
from datetime import datetime
from datetime import date
from datetime import timedelta
from dateutil import rrule
from dateutil.parser import parse
import pandas as pd
import datetime as dt
import sqlite3
import re
import random
import os
import time
import telebot
import emoji
#bot = telebot.TeleBot('5898826480:AAE_HCmCajhiVtdB1Q-Kxu-gRpaEm0qhOOY')
bot = telebot.TeleBot('1877401711:AAF8qEYooYn-gzuYxktLiRQkMQ8jnqoWCCQ')

#def SQLINIT():
sqlite_connection = sqlite3.connect('bot.db', check_same_thread = False)
#    a = '''CREATE TABLE bonds (id INTEGER PRIMARY KEY AUTOINCREMENT, description STRING, name STRING, emitent STRING, couponmin INTEGER, couponcurr STRING, couponprice INTEGER);'''
    #b = '''DROP TABLE bonds;'''
    #c = '''INSERT INTO bonds (description, name, emitent, couponmin, couponcurr, couponprice) VALUES('Cool bond really', 'bebrNco', 'terli', 10, 'Rivals', 10);'''
    #e = '''UPDATE bonds SET couponprice = 11 WHERE name = 'bebrNco';'''
    #f = '''SELECT * FROM bonds WHERE name = 'bebrNco';'''
    #d = '''ALTER TABLE bonds ADD isdef BIT;'''
cursor = sqlite_connection.cursor()
#cursor.execute(d)
    #sqlite_connection.commit()
   # print(cursor.fetchall())
   # cursor.close()
