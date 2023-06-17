import telebot
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import psycopg2

bot = telebot.TeleBot('Здесь должен быть токен бота')

connection = psycopg2.connect(user="Имя пользователя БД",
                                  password='Пароль от пользователя БД',
                                  host="Айпишник БД",
                                  port="5432",
                                  database="Имя БД")
connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = connection.cursor()
print('cursor is', cursor)
print('Соединение с PostgreSQL установлено')
