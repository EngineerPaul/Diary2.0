from telebot import types
from config import MY_ID, SITELINK
import json
from api_requests import (
    send_hour_repeat, send_day_repeat, send_new_reminder, send_info
)
from utils import get_date, get_now_format


def get_info(bot, command):
    @bot.message_handler(commands=[command])
    def get_info(msg):
        # https://habr.com/ru/articles/821661/ - краткое описание инфы в msg
        from_user = {
            'id': MY_ID,  # id чата (у пользователей похоже нет id)
            'is_bot': False,  # это бот?
            'first_name': 'user name',  # имя
            'username': 'user nickname',  # никнейм без собачки @
            'last_name': 'user second name',  # отчество
        }
        # print(msg)  # вся информация о сообщении
        # print(msg.from_user)  # информация о пользователе
        print(msg.text)  # текст сообщения
        print(msg.chat)  # информация о чате
        print(msg.date)  # дата в секундах


def start(bot, command):
    @bot.message_handler(commands=[command])
    def start(msg):
        first_mess = (
            f"Привет, <b>{msg.from_user.first_name}</b>!\n"
            f"Бот получения уведомлений активирован.\n"
            f"В меню (слева внизу) можно быстро создать простое напоминание "
            f"или получить ссылку для перехода на сайт."
        )
        bot.send_message(  # отправляем сообщение пользователю
            msg.chat.id,  # находим чат
            first_mess,  # вставляем сообщение
            parse_mode='html',
        )

        # отправить usr_id в БД для дальнейшей отправки напоминаний по id
        info = {
            'tg_user_id': msg.from_user.id,
        }
        send_info(info)


def send_test(bot, command):
    @bot.message_handler(commands=[command])
    def send_test(msg):
        message = 'Отправка напоминания'

        markup = types.InlineKeyboardMarkup()
        # data = {
        #     'exec': 'test',  # executable function
        #     'reminder_id': 100,  # id напоминания в БД
        #     'user_id': 100,  # id пользователя в БД (на сайте)
        # }
        data = f'test,{100},{100}'
        btn_test = types.InlineKeyboardButton(
            text='test message',
            callback_data=json.dumps(data)
        )

        data = {
            'exec': 'repeat_hour',  # executable function
            'reminder_id': 100,  # id напоминания в БД
            'user_id': 100,  # id пользователя в БД (на сайте)
        }
        data = f'rep_hour,{100},{100}'
        btn_repeat_hour = types.InlineKeyboardButton(
            text='Перенести на час',
            callback_data=json.dumps(data)
        )

        data = {
            'exec': 'repeat_day',  # executable function
            'reminder_id': 100,  # id напоминания в БД
            'user_id': 100,  # id пользователя в БД (на сайте)
        }
        data = f'rep_day,{100},{100}'
        btn_repeat_day = types.InlineKeyboardButton(
            text='Перенести на день',
            callback_data=json.dumps(data)
        )
        markup.add(btn_test)
        markup.add(btn_repeat_hour, btn_repeat_day)
        bot.send_message(
            msg.chat.id,  # находим нужный чат
            message,  # прикрепляем сообщение
            parse_mode='html',  # режим разметки сообщения
            reply_markup=markup  # прикрепляем кнопки
        )


def sitelink(bot, command):
    # link to the site
    @bot.message_handler(commands=[command])
    def send_reminder(msg):
        link = SITELINK
        bot.send_message(
            chat_id=msg.chat.id,
            text=link,
        )


def create_reminder(bot, command):
    @bot.message_handler(commands=[command])
    def create_reminder(msg):
        bot.send_message(  # отправляем сообщение пользователю
            msg.chat.id,  # находим чат
            'Укажите текст напоминания (или отмена)',  # вставляем сообщение
        )
        bot.register_next_step_handler(msg, create_reminder_title, bot)


def create_reminder_title(msg, bot):
    if msg.text.lower() == 'отмена':
        return
    bot.send_message(  # отправляем сообщение пользователю
        msg.chat.id,  # находим чат
        ('Укажите дату формата ДД.ММ.ГГГГ ЧЧ:ММ\n'
         '(или отмена)\n'
         f'Сейчас {get_now_format()}'),  # вставляем сообщение
    )
    bot.register_next_step_handler(msg, create_reminder_date, bot, msg.text)


def create_reminder_date(msg, bot, title):
    if msg.text.lower() == 'отмена':
        return

    date = get_date(msg.text)
    if not date['status']:
        bot.send_message(  # отправляем сообщение пользователю
            msg.chat.id,  # находим чат
            date['details'],  # вставляем сообщение
        )
        bot.register_next_step_handler(msg, create_reminder_date, bot, msg.text)
        return

    response = send_new_reminder(msg.from_user.username, title, date['details'])
    if response:
        bot.send_message(  # отправляем сообщение пользователю
            msg.chat.id,  # находим чат
            'Напоминание успешно создано',  # вставляем сообщение
        )


def callback(bot):
    # handler of all callbacks
    @bot.callback_query_handler(func=lambda call: True)
    def callback(function_call):
        data = function_call.data.split(',')
        data = {
            'exec': data[0],  # executable function
            'reminder_id': data[1],  # id напоминания в БД
            'user_id': data[2],  # id пользователя в БД (на сайте)
        }
        call = data['exec']

        call == 'test' and call_test(bot, function_call)
        call == 'rep_hour' and call_repeat_hour(bot, function_call, data)
        call == 'rep_day' and call_repeat_day(bot, function_call, data)


def call_repeat_hour(bot, function_call, data):
    # перенос напоминания на час
    user_id = data['user_id']
    reminder_id = data['reminder_id']
    response = send_hour_repeat(user_id, reminder_id)

    if response:
        bot.send_message(
            chat_id=function_call.message.chat.id,
            text='Напоминание перенесено на 1 час',
        )


def call_repeat_day(bot, function_call, data):
    # перенос напоминания на день
    user_id = data['user_id']
    reminder_id = data['reminder_id']
    response = send_day_repeat(user_id, reminder_id)

    if response:
        bot.send_message(
            chat_id=function_call.message.chat.id,
            text='Напоминание перенесено на 1 день',
        )


def call_test(bot, callback):
    print('---callback: ', callback)
    # print('---data: ', callback.data)  # сообщение кнопки
    # print('---from_user: ', callback.from_user)  # инфа о пользователе
    # print('---message: ', callback.message)  # инфа о прикрепленном сообщении
    print('---chat: ', callback.message.chat)  # экз. класса Чат
    # print('---chat.id: ', callback.message.json.chat.id)  # id чата
    print('---text: ', callback.message.text)  # текст сообщения перед кнопкой
    print('---inline_keyboard: ', callback.message.reply_markup.keyboard[0][0])  # инфа о кнопке (двумерный список)
    print('---inline_keyboard: ', callback.message.reply_markup.keyboard[0][0].text)  # сообщение кнопки
    print('---inline_keyboard: ', callback.message.reply_markup.keyboard[0][0].callback_data)  # функция
