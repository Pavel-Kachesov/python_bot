import telebot
import time
from telebot import types
import requests
from bs4 import BeautifulSoup


bot = telebot.TeleBot('6277852837:AAFwo3UFpzUV7WCDVeVjIxXKupNxHQyR5LA')


def temperature(message):
    url = "https://pocasi.seznam.cz/praha?lat=50.052&lon=14.541&z=5&f=muni"
    r = requests.get(url)
    bs = BeautifulSoup(r.text, "lxml")
    temp = bs.find('span', class_="d_cG")
    bot.send_message(message.chat.id, f'Now in Prague is {temp.text}', parse_mode='html')


def tickets(message):
    url = "https://www.kiwi.com/en/search/tiles/prague-czechia,vienna-austria/anywhere/anytime/no-return?sortAggregateBy=price"
    r = requests.get(url)
    bs = BeautifulSoup(r.text, "lxml")
    temp = bs.find('span', class_="d_cG")
    bot.send_message(message.chat.id, f'Now in Prague is {temp.text}', parse_mode='html')


def get_sleep(message):
    ti = []
    result = time.localtime(time.time())
    for i in range(1, 6, 1):
        hour = result.tm_hour
        minutes = result.tm_min + i * 30
        while minutes >= 60:
            minutes = minutes - 60
            hour = hour + 1
        if minutes < 10:
            minutes = f'0{minutes}'
        hour = hour + i
        if hour >= 24:
            hour = hour - 24
        tim = f'{hour}:{minutes}'
        ti.append(str(tim))
    bot.send_message(message.chat.id, 'You can wake up at:', parse_mode='html')
    bot.send_message(message.chat.id, '  '.join(ti), parse_mode='html')
    ti.clear()


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    sleep = types.KeyboardButton('Sleep time')
    website = types.KeyboardButton('Cheap tickets')
    weather = types.KeyboardButton('Weather')
    markup.add(sleep, website, weather)
    bot.send_message(message.chat.id, 'Hi, that is button for you', reply_markup=markup)


@bot.message_handler(content_types=["text"])
def get_messages(message):
    if message.text == 'Sleep time':
        get_sleep(message)
    elif message.text == 'Weather':
        temperature(message)
    elif message.text == 'Cheap tickets':
        tickets(message)
    elif message.text == 'Hi':
        mess = f'Hi, {message.from_user.first_name} {message.from_user.last_name}'
        bot.send_message(message.chat.id, mess, parse_mode='html')
    elif message.text == 'ID':
        bot.send_message(message.chat.id, f'Your ID is {message.from_user.id}', parse_mode='html')
    else:
        bot.send_message(message.chat.id, 'Sorry, I dont understand you, please use some botton', parse_mode='html')


bot.polling(none_stop=True)
