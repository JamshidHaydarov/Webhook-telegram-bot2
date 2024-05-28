from django.shortcuts import render
import json
import requests
from django.http import HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
import telebot
import logging
from random import randint
from django.core.mail import send_mail

# Токен телеграм бота
TOKEN = Token
# API ключ с сайта openweathermap.org
API = Api
bot = telebot.TeleBot(TOKEN)
country = None


@csrf_exempt
def bot_view(request):
    if request.method == 'POST':
        update = telebot.types.Update.de_json(request.body.decode("utf-8"))
        try:
            bot.process_new_updates([update])
        except Exception as e:
            logging.error(e)
        return HttpResponse(status=200)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, f'Assalomu aleykum {message.from_user.first_name}, yangiliklar botimizga hush kelibsiz! Ikki harfdan iborat davlat kodini yozib qoldiring!\n\nP.S. O\'zbekiston yangiliklarini korsata olmaymiz!')
    bot.register_next_step_handler(message, get_news)

def get_news(message):
    try:
        global country
        country = message.text.strip()
        res = requests.get(f'https://newsapi.org/v2/top-headlines?country={country}&apiKey={API}')
        data = json.loads(res.text)
        name1 = data["articles"][0]["source"]["name"]
        author1 = data["articles"][0]["author"]
        name2 = data["articles"][1]["source"]["name"]
        author2 = data["articles"][0]["author"]
        name3 = data["articles"][2]["source"]["name"]
        author3 = data["articles"][0]["author"]
        markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
        btn1 = telebot.types.InlineKeyboardButton('1')
        markup.row(btn1)
        btn2 = telebot.types.InlineKeyboardButton('2')
        btn3 = telebot.types.InlineKeyboardButton('3')
        markup.row(btn2, btn3)
        bot.send_message(message.chat.id, f'Name: {name1}\nAuthor: {author1}\n\nName: {name2}\nAuthor: {author2}\n\nName: {name3}\nAuthor: {author3}', reply_markup=markup)
        bot.register_next_step_handler(message, send_news)
    except Exception as s:
        bot.send_message(message.chat.id, f'Hatolik yuz berdi, iltimos qaytatdan yozib qoldiring!\n\nHatolik: {s}')
        bot.register_next_step_handler(message, get_news)

def send_news(message):
    num = int(message.text.strip())
    res = requests.get(f'https://newsapi.org/v2/top-headlines?country={country}&apiKey={API}')
    data = json.loads(res.text)
    name = data["articles"][num]["source"]["name"]
    author = data["articles"][num]["author"]
    content = data["articles"][num]["content"]
    bot.send_message(message.chat.id, f'{name}\n\n{content}\n\n{author}')


