from telebot import types
from config import MY_ID, SITELINK
import json
from api.server.queries import (
    # send_hour_repeat, send_day_repeat,
    send_new_reminder, send_info,
    send_django, send_notice_shift
)
from utils.utils import get_date, get_now_format


def get_info(bot, command):  # выводит ифнормацию из msg (для раработки)
    """ /info - выводит ифнормацию, которая заложена в msg (для раработки) """
    @bot.message_handler(commands=[command])
    def get_info(msg):
        # https://habr.com/ru/articles/821661/ - краткое описание инфы в msg
        # from_user = {  # пример вывода из msg.from_user
        #     'id': MY_ID,  # id чата (у пользователей похоже нет id)
        #     'is_bot': False,  # это бот?
        #     'first_name': 'user name',  # имя
        #     'username': 'user nickname',  # никнейм без собачки @
        #     'last_name': 'user second name',  # отчество
        # }
        # print(msg)  # вся информация о сообщении
        # print(msg.from_user)  # информация о пользователе
        print(msg.text)  # текст сообщения
        print(msg.chat)  # информация о чате
        print(msg.date)  # дата в секундах


def start(bot, command):  # стартовая команда при запуске бота
    """ /start - обработка включения бота у польователя. Сохранение инфы об
    аккаунте в БД """
    @bot.message_handler(commands=[command])
    def start(msg):
        user_id = msg.text.split(' ')[1]
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
        user_info = {
            'user_id': user_id,
            'tg_user_id': msg.from_user.id,
            'tg_username': msg.from_user.username,
            'chat_id': msg.chat.id,
        }

        # Отправляем информацию на сервер и проверяем результат
        registration_success = send_info(user_info)

        if registration_success:
            bot.send_message(
                chat_id=msg.chat.id,
                text="Регистрация завершена",
                parse_mode='html'
            )
        else:
            bot.send_message(
                chat_id=msg.chat.id,
                text="Ошибка при регистрации. Попробуйте снова.",
                parse_mode='html'
            )


def send_test(bot, command):  # шаблон для ручной отправки напоминания
    """ /send (debug==True) отправляет уведомление с кнопками перенести на час и день """
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


def sitelink(bot, command):  # ссылка на сайт (тест)
    """отправка ссылки с гиперссылкой"""
    @bot.message_handler(commands=[command])
    def send_reminder(msg):
        link = f'<a href="{SITELINK}">Ссылка на сайт</a>'
        bot.send_message(
            chat_id=msg.chat.id,
            text=link,
            parse_mode='html'
        )


def create_reminder(bot, command):  # создание нового уведомления
    """ Создание нового уведомления по кнопке в меню. Можно создать только
    одиночное уведомление """
    @bot.message_handler(commands=[command])
    def create_reminder(msg):
        bot.send_message(  # отправляем сообщение пользователю
            msg.chat.id,  # находим чат
            'Укажите текст напоминания (или отмена)',  # вставляем сообщение
        )
        bot.register_next_step_handler(msg, create_reminder_title, bot)


def create_reminder_title(msg, bot):  # создание нового уведомления (шаг 2)
    """ Запускается последователно при создании уведомления.
    Сохраняет заголовок """
    if msg.text.lower() == 'отмена':
        return
    bot.send_message(  # отправляем сообщение пользователю
        msg.chat.id,  # находим чат
        ('Укажите дату формата ДД.ММ.ГГГГ ЧЧ:ММ\n'
         '(или отмена)\n'
         f'Сейчас {get_now_format()}'),  # вставляем сообщение
    )
    bot.register_next_step_handler(msg, create_reminder_date, bot, msg.text)


def create_reminder_date(msg, bot, title):  # создание нового уведомления (шаг 3)
    """ Запускается последователно при создании уведомления.
    Сохраняет дату """
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

    response = send_new_reminder(msg.from_user.username, title, date['details'], msg.chat.id)
    if response:
        bot.send_message(  # отправляем сообщение пользователю
            msg.chat.id,  # находим чат
            'Напоминание успешно создано',  # вставляем сообщение
        )
    else:
        bot.send_message(  # отправляем сообщение пользователю
            msg.chat.id,  # находим чат
            'Ошибка создания напоминания',  # вставляем сообщение
        )


def callback(bot):  # обработчик всех inline кнопок
    """ Обрабатывает события всех inline кнопок (например, в напоминаниях
    send_test)"""
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

        # вызов функций справа, если выполняются условия слева
        call == 'test' and call_test(bot, function_call)
        call == 'rep_hour' and call_repeat_hour(bot, function_call, data, function_call.message.chat.id)
        call == 'rep_day' and call_repeat_day(bot, function_call, data, function_call.message.chat.id)


def call_repeat_hour(bot, function_call, data, chat_id):  # перенос напоминания на час
    """Перенос конкретного напоминания на час при нажатии inline-кнопки"""
    user_id = int(data['user_id'])
    reminder_id = int(data['reminder_id'])
    # response = send_hour_repeat(user_id, reminder_id)
    response = send_notice_shift(user_id, reminder_id, 'day', chat_id)

    if response:
        bot.send_message(
            chat_id=function_call.message.chat.id,
            text='Напоминание перенесено на 1 час',
        )
    else:
        bot.send_message(  # отправляем сообщение пользователю
            chat_id,  # находим чат
            'Ошибка изменения напоминания',  # вставляем сообщение
        )


def call_repeat_day(bot, function_call, data, chat_id):  # перенос напоминания на день
    """Перенос конкретного напоминания на день при нажатии inline-кнопки"""
    user_id = int(data['user_id'])
    reminder_id = int(data['reminder_id'])
    # response = send_day_repeat(user_id, reminder_id)
    response = send_notice_shift(user_id, reminder_id, 'hour', chat_id)

    if response:
        bot.send_message(
            chat_id=function_call.message.chat.id,
            text='Напоминание перенесено на 1 день',
        )
    else:
        bot.send_message(  # отправляем сообщение пользователю
            chat_id,  # находим чат
            'Ошибка изменения напоминания',  # вставляем сообщение
        )


def call_test(bot, callback):  # тестовая функция inline-кнопки
    """Тестовая функция для отладки. Срабатывает при нажатии на inline
    кнопку конкретного уведомления с надписью "test message" (send_test)"""
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


def test_to_django(bot, command):  # тестовая отправка http
    """ /testdajngo_get - Тестовая функция отправки уведомления на
    fastapi (и потом django) """
    @bot.message_handler(commands=[command])
    def test_to_django(msg):
        # /testdajngo_get
        print('Сообщение обработано')
        # https://habr.com/ru/articles/821661/ - краткое описание инфы в msg
        # from_user = {  # пример вывода из msg.from_user
        #     'id': MY_ID,  # id чата (у пользователей похоже нет id)
        #     'is_bot': False,  # это бот?
        #     'first_name': 'user name',  # имя
        #     'username': 'user nickname',  # никнейм без собачки @
        #     'last_name': 'user second name',  # отчество
        # }
        # print(msg)  # вся информация о сообщении
        # print(msg.from_user)  # информация о пользователе
        print(msg.text)  # текст сообщения
        print(msg.chat)  # информация о чате
        print(msg.date)  # дата в секундах

        send_django(msg)  # отправка http
