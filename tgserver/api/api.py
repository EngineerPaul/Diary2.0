from datetime import datetime, timedelta
import aiohttp

from fastapi import APIRouter, Response, Depends
from fastapi.responses import JSONResponse

from api.schemas import (
    ReminderCreater, TestDjango,
    NewNoticeSchema, NoticeShiftSchema, UserInfoSchema, NoticeListSchema
)
from queries.to_tgbot import send_msg_bot
from queries.to_server import (
    send_test_to_Django,
    send_create_notice, send_notice_shift, send_userinfo
)
from config import MY_TG_ID
from dependencies import get_session
# from services import RemindData


router = APIRouter()


@router.post(
    "/bot/create-notice/",
    tags=['From TG'],
    summary="Create new reminder using the TG bot"
)
async def create_notice_api(  # создание нового уведомления через бота
    data: NewNoticeSchema,
    session: aiohttp.ClientSession = Depends(get_session)
):
    server_response = await send_create_notice(data, session)  # отпправить HTTP запрос на сервер
    if server_response:
        response = JSONResponse(
            content={'success': True},
            status_code=201,
            media_type="application/json"
        )
    else:
        response = JSONResponse(
            content={'success': False},
            status_code=400,
            media_type="application/json"
        )
    return response


@router.post(
    "/bot/notice-shift/",
    tags=['From TG'],
    summary="Rescheduling the notice to the next hour/day"
)
async def notice_shift_api(  # Смещение уведомления на час/день
    data: NoticeShiftSchema,
    session: aiohttp.ClientSession = Depends(get_session)
):
    server_response = await send_notice_shift(data, session)  # отпправить HTTP запрос на сервер
    server_response = None
    if server_response:
        response = Response(
            content={'success': True},
            status_code=200,
            media_type="application/json"
        )
    else:
        response = Response(
            content={'success': False},
            status_code=400,
            media_type="application/json"
        )
    return response


@router.post(
    "/bot/create-user/",
    tags=['From TG'],
    summary="Saving user info during registration"
)
async def userinfo_api(  # сохранение инфы о пользователе (хз, где)
    data: UserInfoSchema,
    session: aiohttp.ClientSession = Depends(get_session)
):
    server_response = await send_userinfo(data, session)  # отпправить HTTP запрос на сервер
    server_response = None
    if server_response:
        response = Response(
            content={'success': True},
            status_code=200,
            media_type="application/json"
        )
    else:
        response = Response(
            content={'success': False},
            status_code=400,
            media_type="application/json"
        )
    return response


@router.post(
    "/bot/set-notice-list/",
    tags=['From Django server'],
    summary="Create new reminder using the TG bot"
)
async def get_notice_list_api(data: NoticeListSchema):  # получение списка уведомлений от сервера
    # RemindData.set_reminders_list(data.notice_list)
    # RemindData.set_date(data.next_date)

    response = Response(
        content={'success': True},
        status_code=200,
        media_type="application/json"
    )
    return response


@router.post(
    "/test-send",
    tags=['test'],
    summary="Send test msg to the TG bot"
)
async def test_query():  # отправить сообщение в чат бота
    """ Quilcky check of sending msg to the TG bot """

    await send_msg_bot(
        chat_id=MY_TG_ID,
        text='Какой-то текст из API',  # можно дополнить любой информацией
        user_id=100,
        reminder_id=100
    )

    return {"detail": "success"}


@router.get(
    "/test-django/",
    tags=['test-django'],
    summary="Получение post запроса от Django"
)
async def test_dajngo_get():  # получение тестового get запроса от backend
    """  """

    print('Получен get запрос от Django')
    # await send_msg_bot(
    #     chat_id=MY_TG_ID,
    #     text='Какой-то текст из API',  # можно дополнить любой информацией
    #     user_id=100,
    #     reminder_id=100
    # )

    return {"detail": "success"}


@router.post(
    "/test-django/",
    tags=['test-django'],
    summary="Получение post запроса от Django"
)
async def test_dajngo_post(req: TestDjango):  # получение тестового post запроса от backend
    """  """

    print('Получен post запрос от Django')
    print(req)
    # await send_msg_bot(
    #     chat_id=MY_TG_ID,
    #     text='Какой-то текст из API',  # можно дополнить любой информацией
    #     user_id=100,
    #     reminder_id=100
    # )

    return {"detail": "success"}


@router.post(
    "/from-tg-to-django/",
    tags=['from-tg-to-django'],
    summary="Передача запроса от TG в Django"
)
async def test_dajngo_post(session: aiohttp.ClientSession = Depends(get_session)):  # тестовая передача запроса от TG в backend
    """ Передача тестового запроса от TG-bot в server (Django) """

    print('Получен post запрос от TG')
    await send_test_to_Django(data='data', session=session)
    # await send_msg_bot(
    #     chat_id=MY_TG_ID,
    #     text='Какой-то текст из API',  # можно дополнить любой информацией
    #     user_id=100,
    #     reminder_id=100
    # )

    return {"detail": "success"}


# рабочий запрос в чат (отключен на windows)
# @router.post(
#     "/test-celery-beat",
#     tags=['test'],
#     summary="Set a test reminder list. Send a msg in 30s"
# )
# async def test_celery():
#     """ Quickly check the work of the reminders list """

#     RemindData.set_reminders_list([
#         {
#             'user_id': 100,
#             'reminder_id': 100,
#             'message': 'Тестовое напоминание',
#             'tg_id': MY_TG_ID,
#         },
#     ])
#     RemindData.set_date(
#         datetime.now() + timedelta(seconds=30)
#     )

#     return {"detail": "success"}
