from core import logging, yaml, os
from telebot import types, TeleBot

def editor_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for i in os.listdir("known_groups"):
        keyboard.add(i)
    keyboard.add("Назад")
    return keyboard

def editor_subjects_keyboard(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for i in yaml.safe_load(open(f"known_groups/{message.text}/{message.text}_subjects.yml")):
        keyboard.add(i)
    keyboard.add("Назад")
    return keyboard


def return_to_main():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add("Что у нас завтра?")
    return keyboard

def editor(message, bot: TeleBot):
    logging.debug(f"Called editor from {message.chat.id}")
    try:
        if yaml.safe_load(open(f"chats/{message.chat.id}"))["staff"]:
            keyboard = editor_keyboard()
            keyboard.add("Добавить")
            keyboard.add("Назад")
            bot.send_message(message.chat.id, "Какую группу редактируем?", reply_markup=keyboard)
            bot.register_next_step_handler(message, editor_action, bot)
        else:
            bot.send_message(message.chat.id, "Оперция не позволена.", reply_markup=return_to_main())
    except KeyError:
        bot.send_message(message.chat.id, "Оперция не позволена.", reply_markup=return_to_main())


def editor_action(message, bot):
    if message.text == "Назад":
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add("Что у нас завтра?")
        bot.send_message(message.chat.id, "Отмена.", reply_markup=keyboard)
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add("Расписание")
        keyboard.add("Предметы")
        keyboard.add("Назад")
        bot.register_next_step_handler(message, edit_group, bot, message.text)
        bot.send_message(message.chat.id, "Что будем редактировать?", reply_markup=keyboard)

def edit_group(message, bot, group):
    if message.text == "Назад":
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add("Что у нас завтра?")
        bot.send_message(message.chat.id, "Отмена.", reply_markup=keyboard)
    else:
        if message.text == "Расписание":
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            keyboard.add("Понедельник")
            keyboard.add("Вторник")
            keyboard.add("Среда")
            keyboard.add("Четверг")
            keyboard.add("Пятница") 
            keyboard.add("Суббота")
            keyboard.add("Назад")
            bot.register_next_step_handler(message, edit_timetable, bot, group)
            bot.send_message(message.chat.id, "Выберите день недели", reply_markup=keyboard)
        elif message.text == "Предметы":
            bot.register_next_step_handler(message, edit_subject, bot, group)
            bot.send_message(message.chat.id, "Выберите предмет", reply_markup=editor_subjects_keyboard(message))

def edit_timetable(message, bot, group):
    if message.text == "Назад":
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add("Что у нас завтра?")
        bot.send_message(message.chat.id, "Отмена.", reply_markup=keyboard)
    wd = {"Понедельник": 1, "Вторник": 2, "Среда": 3, "Четверг": 4, "Пятница": 5, "Суббота": 6}
    if message.text in wd.keys():
        bot.register_next_step_handler(message, save_timetable, bot, group, wd[message.text])
        bot.send_message(message.chat.id, f"""
Отправьте новое расписание на {wd[message.text]} в следующем формате:
```
1 ; номера недель через запятую (или "четные"/"нечетные"/"все") ; предмет в 9:20 ; пз/лекция
1 ; другие номера недель через запятую ; предмет в 9:20 ; пз/лекция
2 ; номера недель через запятую ; предмет в 11:00 ; пз/лекция
2 ; другие номера недель через запятую ; предмет в 11:00 ; пз/лекция
3 ; номера недель через запятую ; предмет в 13:30 ; пз/лекция 
3 ; другие номера недель через запятую ; предмет в 13:30 ; пз/лекция
4 ; номера недель через запятую ; предмет в 15:10 ; пз/лекция
4 ; другие номера недель через запятую ; предмет в 15:10 ; пз/лекция
```
Предмет указывать одним словом ; например, анатомия\\.

Примеры:

```
1 ; все ; анатомия ; пз
2 ; все ; анатомия ; пз
3 ; все ; ничего
4 ; все ; ничего
````

``` 
1 ; четные ; гистология ; пз
1 ; нечетные ; биохимия ; пз
2 ; четные ; гистология ; пз
2 ; нечетные ; биохимия ; пз
3 ; все ; ничего
4 ; все ; ничего

```

""", parse_mode="MarkdownV2", reply_markup=types.ReplyKeyboardRemove())

def save_timetable(message, bot, group, wd):
    if message.text == "Назад":
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add("Что у нас завтра?")
        bot.send_message(message.chat.id, "Отмена.", reply_markup=keyboard)
    else:
        tt = message.text.split('\n')
        out = [dict(), dict(), dict(), dict()]
        for i in tt:
            if i[1] == "четные":
                i[1] = "even"
            elif i[1] == "нечетные":
                i[1] = "odd"
            elif i[1] == "все":
                i[1] = "every"
            i = i.split(' ; ')
            out[wd[i[0]]][i[1]] = i[2]
        for i in tt:
            i = i.split(';')
            if i[0] == '1':
                out[0][i[1]] = f"{i[3]}_{i[2]}"
            elif i[0] == '2':
                out[1][i[1]] = f"{i[3]}_{i[2]}"
            elif i[0] == '3':
                out[2][i[1]] = f"{i[3]}_{i[2]}"
            elif i[0] == '4':
                out[3][i[1]] = f"{i[3]}_{i[2]}"
        with open(f"known_groups/{group}/{group}_{wd}_tt.yml", 'w') as f:
            yaml.dump(out, f)


def edit_subject(message, bot, group):
    if message.text == "Назад":
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add("Что у нас завтра?")
        bot.send_message(message.chat.id, "Отмена.", reply_markup=keyboard)
    else:
        bot.register_next_step_handler(message, save_subject, bot, group, message.text)
        bot.send_message(message.chat.id, f"""
Отправьте информацию о предмете в формате:
```yaml
name: название предмета
пз:
  place: место 
  auditory: аудитория
лекция:
  place: место
  auditory: аудитория
```
Если по предмету нет лекций, напишите ";" в графы place и auditory для лекции\\.                      
```""", reply_markup=types.ReplyKeyboardRemove(), parse_mode="MarkdownV2")

def save_subject(message, bot, group, subject):
    if message.text == "Назад":
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add("Что у нас завтра?")
        bot.send_message(message.chat.id, "Отмена.", reply_markup=keyboard)
    else:
        with open(f"known_groups/{group}/{group}_subjects.yml", 'r') as f:
            subjects = yaml.safe_load(f)
        try: 
            sbj = yaml.safe_load(message.text)
        except yaml.YAMLError:
            bot.send_message(message.chat.id, "Некорректный формат.")
            return

        subjects[subject] = sbj
        with open(f"known_groups/{group}/{group}_subjects.yml", 'w') as f:
            yaml.dump(subjects, f)