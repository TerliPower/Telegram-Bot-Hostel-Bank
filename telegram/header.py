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
import logging


botname = '@simpleroll_bot'

sqlite_connection = sqlite3.connect('bot.db', check_same_thread = False)
cursor = sqlite_connection.cursor()

logging.basicConfig(level=logging.DEBUG, filename='BOTLOG',filemode='w')
