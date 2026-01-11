from datetime import datetime

from .client import api_client, api_tg_client, api_auth_client


# def send_hour_repeat(user_id: int, reminder_id: int) -> bool:  # перенос уведомления на час
#     """ Cмещение уведомления на час """
#     url = 'tgapi/bot/hour-shift/'
#     body = {
#         'user_id': user_id,
#         'reminder_id': reminder_id,
#     }
#     response = api_tg_client.post(url, body)
#     # на сервере напоминание (снова) активируется, а исполнение переносится на now+1час
#     if response:
#         return True
#     else:
#         return False


# def send_day_repeat(user_id: int, reminder_id: int) -> bool:  # смещение уведомления на день
#     """ Cмещение уведомления на день """
#     url = 'tgapi/bot/day-shift/'
#     body = {
#         'user_id': user_id,
#         'reminder_id': reminder_id,
#     }
#     response = api_tg_client.post(url, body)
#     # на сервере напоминание (снова) активируется, а исполнение переносится на now+1день
#     if response:
#         return True
#     else:
#         return False


def send_new_reminder(username: str, title: str, date: datetime, chat_id: int) -> bool:  # создание нового уведомления
    """ Cоздание нового уведомления """
    url = 'tgapi/bot/create-notice/'
    body = {
        'username': username,
        'title': title,
        'date': date.isoformat(),  # datetime
        'chat_id': chat_id,
    }
    # print('send_new_reminder')
    # print('username: @', username, '\ntitle: ', title, '\ndate: ', date)
    response = api_tg_client.post(url, body)
    # на сервере напоминание (снова) активируется, а исполнение переносится на now+1день
    if response:
        return True
    else:
        return False


def send_notice_shift(user_id: int, reminder_id: int, mode: str, chat_id: int) -> bool:  # смещение уведомления на день
    """ Cмещение уведомления на день """
    url = 'tgapi/bot/notice-shift/'
    if not (mode == 'day' or mode == 'hour'):
        print('Error: wrong mode')
        return None

    body = {
        'user_id': user_id,
        'reminder_id': reminder_id,
        'mode': mode,
        'chat_id': chat_id,
    }
    response = api_tg_client.post(url, body)
    # на сервере напоминание (снова) активируется, а исполнение переносится на now+1день
    if response:
        return True
    else:
        return False


# async def send():  # похоже, какой-то тест, хз

#     url = f'http://127.0.0.1:8000/tgapi/reminders'
#     body = ''
#     body = {
#         "nickname": "@string",
#         "title": "string",
#         "mode": "hour",
#         "date": "2025-09-30T22:15:22"
#     }

#     print(body)
#     import aiohttp
#     async with aiohttp.ClientSession() as session:  # в реальных приложениях его обычно создают один раз и используют многократно
#         async with session.post(url, json=body) as resp:
#             res = await resp.text()
#             print(f'Закончил выполнение: {res}')
#             return res

#     # быстрое создание напоминания
#     # print('send_new_reminder')
#     # print('username: @', username, '\ntitle: ', title, '\ndate: ', date)
#     return True


def send_info(info: dict) -> bool:  # отправка инфы о чате на сервер при активации бота
    """ Отправка инфы о чате на сервер при активации бота """
    url = 'tgapi/bot/create-user/'
    body = info
    response = api_tg_client.post(url, body)
    if response:
        return True
    else:
        return False


def send_django(data: dict) -> bool:  # тестовая отправка http на сервер (/)
    """ Отправка данных на Django сервер через FastAPI """
    url = 'tgapi/from-tg-to-django'
    body = {
        'msg': 'Works! from tg',
        # 'data': data  # используем переданные данные
    }
    response = api_tg_client.post(url, body)
    return response
