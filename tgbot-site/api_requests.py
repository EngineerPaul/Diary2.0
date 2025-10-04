import asyncio
import aiohttp


def send_hour_repeat(user_id, reminder_id):
    # перенос напоминания на час
    # отправить запрос на сервер с указанием reminder_id
    # на сервере напоминание (снова) активируется, а исполнение переносится на now+1час
    return True  # status code


def send_day_repeat(user_id, reminder_id):
    # перенос напоминания на день
    # отправить запрос на сервер с указанием reminder_id
    # на сервере напоминание (снова) активируется, а исполнение переносится на now+1день
    return True


def send_new_reminder(username, title, date):
    # быстрое создание напоминания
    asyncio.run(send())
    # res = send()
    # asyncio.run(send())
    print('send_new_reminder')
    print('username: @', username, '\ntitle: ', title, '\ndate: ', date)
    return True


async def send():

    url = f'http://127.0.0.1:8000/tgapi/reminders'
    body = ''
    body = {
        "nickname": "@string",
        "title": "string",
        "mode": "hour",
        "date": "2025-09-30T22:15:22"
    }

    print(body)
    async with aiohttp.ClientSession() as session:  # в реальных приложениях его обычно создают один раз и используют многократно
        async with session.post(url, json=body) as resp:
            res = await resp.text()
            print(f'Закончил выполнение: {res}')
            return res

    # быстрое создание напоминания
    # print('send_new_reminder')
    # print('username: @', username, '\ntitle: ', title, '\ndate: ', date)
    return True


def send_info(info):
    # отправка инфы о пользователе на сервер при активации бота
    return True
