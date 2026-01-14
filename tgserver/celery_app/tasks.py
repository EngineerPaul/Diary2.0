from datetime import datetime
import asyncio

from celery_client import celery_app
from services import RemindData
from queries.to_tgbot import send_msg_bot
from queries.to_server import send_mailing_list_report


# @celery_app.task  # worker test
# def celery_test():
#     print('------------------------Celery работает')


# @celery_app.task  # beat test
# def celery_every_5s():
#     print('------------------------Celery работает каждые 5 секунд')


@celery_app.task  # beat
def celery_check_dispatch_date():
    """ Проверка даты отправки сообщений (10 сек) """

    dispatch_date = RemindData.get_date()
    if dispatch_date is None:
        print('Сообщений для отправки нет')
        return
    now = datetime.now()
    if now > dispatch_date:
        # отправка списка сообщений
        send_all_reminders.delay()
    else:
        print(f'Отправка через {dispatch_date - now} секунд')


@celery_app.task  # worker
def send_all_reminders():
    """ Отправка списка напоминаний воркером.
    Получение нового списка от сервера """

    rem_list = RemindData.get_reminders_list()
    if rem_list is None:
        print('Error: список сообщений пуст')
        return
    for rem in rem_list:
        asyncio.run(
            send_msg_bot(
                chat_id=rem['tg_id'],
                text=rem['message'],
                user_id=rem['user_id'],
                reminder_id=rem['reminder_id'],
            )
        )
    print('Сообщения отправлены')
    RemindData.set_reminders_list(None)
    RemindData.set_date(None)

    # отправка отчета серверу
    send_mailing_list_report(rem_list)
