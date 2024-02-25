import telebot
import os
import yaml

def start(message, bot):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for i in os.listdir("known_groups"):
        keyboard.add(i) if i != "places.yml" else None
    bot.register_next_step_handler(message, save_group, bot=bot)
    bot.send_message(
        message.chat.id,
        f'Привет, {message.from_user.first_name}. Выбери номер группы!',
        reply_markup=keyboard)


def save_group(message, bot):
    if message.chat.id not in os.listdir("chats"):
        file = open(f"chats/{message.chat.id}", "a+")
        chat = {"group": message.text}
    else:
        file = open(f"chats/{message.chat.id}", "w+")
        chat = yaml.safe_load(file)
        chat["group"] = message.text
        chat["staff"] = False
    file.write(yaml.safe_dump(chat))
    file.close()
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Что у нас завтра?")
    bot.reply_to(message, f"Установлена группа {message.text}", reply_markup=keyboard)