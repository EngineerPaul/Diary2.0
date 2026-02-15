import socket
import time
from datetime import datetime, timedelta
import pytz

from config import MAX_YEAR
from api.server.queries import get_userinfo


def get_date(str_date: str) -> dict:
    """ Check a date format. Format must be like ДД.ММ.ГГГГ ЧЧ:ММ.
    (like '30.01.2001 10.00') """

    # str_date = '30.01.2001 10.00'
    if len(str_date) != 16:
        return {
            'status': False,
            'details': 'Неверный формат даты.\nПопробуйте снова (или отмена)'
        }
    try:
        day = int(str_date[0:2])
        month = int(str_date[3:5])
        year = int(str_date[6:10])
        hour = int(str_date[11:13])
        minute = int(str_date[14:16])
    except BaseException:
        return {
            'status': False,
            'details': 'Неверный формат даты.\nПопробуйте снова (или отмена)'
        }

    date = datetime(year, month, day, hour, minute)
    if date < datetime.now():
        return {
            'status': False,
            'details': 'Нельзя указывать прошедшую дату.\nПопробуйте снова (или отмена)'
        }

    if date > datetime.now() + timedelta(365*MAX_YEAR):
        return {
            'status': False,
            'details': f'Предел даты - {MAX_YEAR} лет.\nПопробуйте снова (или отмена)'
        }

    return {
            'status': True,
            'details': date
        }


def get_now_format(chat_id: int) -> str:
    """ Get now date like 'ДД.ММ.ГГГГ ЧЧ:ММ' format """

    user_info = get_userinfo(chat_id)  # from authserver
    timezone = user_info['timezone']
    if timezone:
        # Создаем datetime без указания часового пояса
        utc_datetime = datetime.now()
        # Соединяем datetime и UTC
        utc_datetime = pytz.UTC.localize(utc_datetime)
        # Конвертируем в часовой пояс пользователя
        user_datetime = utc_datetime.astimezone(pytz.timezone(timezone))
        now = user_datetime
    else:
        now = datetime.now()

    formated_now = (f'{now.day:0>{2}}.{now.month:0>{2}}.{now.year} '
                    f'{now.hour:0>{2}}.{now.minute:0>{2}}')
    return formated_now


def check_connection(tries: int = 5):
    """ Checking internet connection.
    The docker container establishes a connection with a delay. """

    for _ in range(tries):
        try:
            sock = socket.create_connection(("www.google.com", 80))
        except BaseException:
            print('Error: connection not established. Try again in 3s')
            time.sleep(3)
        else:
            print('Internet connection established successfully')
            # print(f'Socket: {sock}')
            sock.close()
            break
