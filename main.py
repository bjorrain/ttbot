
import yaml
import datetime
import os
import schedule
from threading import Thread
import time
from core import logging, print
import telebot
from telebot import types, TeleBot
from timetables import send_for_date, send_no_message
from user_management import start as botstart
from editor import editor

with open("config.yml") as f:
        config = yaml.safe_load(f)
        TOKEN = config["TOKEN"]

bot = telebot.TeleBot(TOKEN)



places = yaml.safe_load(open("known_groups/places.yml"))


@bot.message_handler(commands=["tomorrow"])
@bot.message_handler(func=lambda message: message.text.lower() == "что у нас завтра?")
def tomorrow(message):
    send_for_date(message=message, bot=bot, date=datetime.date.today() + datetime.timedelta(days=1))

@bot.message_handler(commands=["start"])
def start(message):
    botstart(message, bot)

@bot.message_handler(commands=["editor"])
def sudoedit(message):
    editor(message, bot)
def waitress():
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":

    for i in os.listdir("chats"):
        schedule.every().day.at("20:09").do(send_no_message, i, datetime.date.today() + datetime.timedelta(days=1))
    Thread(target=waitress).start()
    bot.polling() 
