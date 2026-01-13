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

    print('send_create_notice: Отправка сообщения в backend')
    async with session.post(url, json=data.dict()) as resp:
        res = await resp.text()
        return res


async def send_notice_shift(data: NoticeShiftSchema, session):  # сдвиг notice
    """ Shifting the notice to the next hour/day using tg bot """

    url = PROJECT_HOSTS['backend'] + 'api/tg-server/notice-shift/'

    print('send_notice_shift: Отправка сообщения в backend')
    async with session.post(url, json=data.dict()) as resp:
        res = await resp.text()
        return res


async def send_userinfo(data: UserInfoSchema, session):  # сохранение инфы пользователя
    """ Saving the user info using tg bot """

    url = PROJECT_HOSTS['backend'] + 'api/tg-server/save-user-info/'

    print('send_userinfo: Отправка сообщения в backend?')
    async with session.post(url, json=data.dict()) as resp:
        res = await resp.text()
        return res


async def send_mailing_list_report(data: dict, session):  # отправка отчета о рассылке напоминаний
    """ Sending the mailing list report to the backend """

    url = PROJECT_HOSTS['backend'] + 'api/tg-server/mailing-list-report/'

    print('send_mailing_list_report: Отправка сообщения в backend')
    async with session.post(url, json=data) as resp:
        res = await resp.text()
        return res
