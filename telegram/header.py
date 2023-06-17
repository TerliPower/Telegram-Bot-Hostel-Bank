from glob import glob
from random import randint
from telebot import types
from os.path import exists
from mybot import bot, cursor
from threading import Thread
from pars import *
from auto import *
import re
import random
import os
import time
import telebot
import logging

bot = telebot.TeleBot('Здесь должен быть токен бота')
botname = '@Здесь должна быть тг ссылка на бота'

pars = Thread(target = RRBot.replenishment_check)
auto = Thread(target = mainl)
pars.start()
print('pars had started')
auto.start()
print('auto had started')

logging.basicConfig(level=logging.DEBUG, filename='BOTLOG',filemode='w')
