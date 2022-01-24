import telebot
import data_for_start

from datetime import date
from data_for_start import sheets_id
import gspread

import os

bot= telebot.TeleBot(data_for_start.bot_token)
google = gspread.service_account()

@bot.message_handler(commands=['start','help'])
def send_welcome (message):
    bot.reply_to(message,"Здравстуйте!" 
                         "\n📝/in - Внести данные"
                         "\n📊/out - Анализ данных"
                         "\n📈/graphics - Графики")