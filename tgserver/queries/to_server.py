from api.schemas import (
    NewNoticeSchema, NoticeShiftSchema, UserInfoSchema
)
from config import PROJECT_HOSTS


# async def send_test_to_Django(data):
#    """ Тестовый запрос на сервер с созданием новой сессии """

#     url = 'http://127.0.0.1:8002/api/tests/from-fastapi/'
#     body = {
#         'msg': 'Works! from fastapi'
#     }

#     async with aiohttp.ClientSession() as session:  # в реальных приложениях его обычно создают один раз и используют многократно
#         async with session.post(url, json=body) as resp:
#             res = await resp.text()
#             # print(f'Закончил выполнение: {res}')
#             return res

async def send_test_to_Django(data, session):
    """ Тестовый запрос на сервер с использованием сессии """

    url = 'http://127.0.0.1:8002/api/tests/from-fastapi/'
    body = {
        'msg': 'Works! from fastapi'
    }

    async with session.post(url, json=body) as resp:
        res = await resp.text()
        # print(f'Закончил выполнение: {res}')
        return res


async def send_create_notice(data: NewNoticeSchema, session):  # создание notice
    """ Creating the new notice using tg bot """

    url = PROJECT_HOSTS['backend'] + 'api/tg-server/new-notice/'

    async with session.post(url, json=data.dict()) as resp:
        res = await resp.text()
        return resp.status, res


async def send_notice_shift(data: NoticeShiftSchema, session):  # сдвиг notice
    """ Shifting the notice to the next hour/day using tg bot """

    url = PROJECT_HOSTS['backend'] + 'api/tg-server/notice-shift/'

    async with session.post(url, json=data.dict()) as resp:
        res = await resp.text()
        return resp.status, res


async def send_userinfo(data: UserInfoSchema, session):  # сохранение инфы пользователя
    """ Saving user info into auth server using tg bot """

    url = PROJECT_HOSTS['auth_server'] + 'api/tg-auth/save'

    async with session.post(url, json=data.dict()) as resp:
        res = await resp.text()
        return resp.status, res


async def send_mailing_list_report(data: dict, session):  # отправка отчета о рассылке напоминаний
    """ Sending the mailing list report to the backend """

    url = PROJECT_HOSTS['backend'] + 'api/tg-server/mailing-list-report/'

    async with session.post(url, json=data) as resp:
        if resp.status != 200:
            print("Error: send_mailing_list_report doesn't work")
        return
