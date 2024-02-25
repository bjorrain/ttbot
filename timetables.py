from ttparser import generate_timetable
import yaml
import datetime
from core import logging
from telebot import types, TeleBot
places = yaml.safe_load(open("known_groups/places.yml"))

def generate_for_date(id, date: datetime.date, places: dict):
    day = date
    week = day.isocalendar().week - 4
    weekday = day.isocalendar().weekday
    with open(f"chats/{id}") as file:
        group = yaml.safe_load(file)["group"]
    if not group:
        return "Сначала выбери группу"
    if weekday == 7:
        text = "Завтра выходной!!"
        return text
    text = f"""
На {day.strftime("%d %B %Y")} у группы {group} расписание такое:
{generate_timetable(weekday, week, group, places)}
    """
    return text

def send_for_date(message, bot: TeleBot, date: datetime.date = datetime.date.today() + datetime.timedelta(days=1)):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Что у нас завтра?")
    bot.send_message(message.chat.id, generate_for_date(message.chat.id, date, places), reply_markup=keyboard)
def send_no_message(id, bot: TeleBot, date: datetime.date = datetime.date.today() + datetime.timedelta(days=1)):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Что у нас завтра?")
    bot.send_message(id, generate_for_date(id, date, places), reply_markup=keyboard)
