from datetime import datetime, timedelta

from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse
from schemas import (
    ReminderCreater, TestDjango,
    NewNoticeSchema, NoticeShiftSchema, UserInfoSchema, NoticeListSchema
)
from queries_tg import send_msg_bot
from queries_serv import (
    send_test_to_Django,
    send_create_notice, send_notice_shift, send_userinfo
)
from config import MY_TG_ID
# from services import RemindData


router = APIRouter()


@router.post(
    "/bot/create-notice/",
    tags=['From TG'],
    summary="Create new reminder using the TG bot"
)
async def create_notice_api(data: NewNoticeSchema):  # создание нового уведомления через бота
    server_response = await send_create_notice(data)  # отпправить HTTP запрос на сервер
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
async def notice_shift_api(data: NoticeShiftSchema):  # Смещение уведомления на час/день
    server_response = send_notice_shift(data)  # отпправить HTTP запрос на сервер
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
async def userinfo_api(data: UserInfoSchema):  # сохранение инфы о пользователе (хз, где)
    server_response = send_userinfo(data)  # отпправить HTTP запрос на сервер
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



# @router.post(
#     "/reminders",
#     tags=['From TG'],
#     summary="Create new reminder using the TG bot"
# )
# async def create_reminder(reminder: ReminderCreater):  # тест (удалить!)
#     """ Create new reminder using the TG bot """

#     # переотправка напоминания на основной сервер
#     # сервер сохраняет и проверяет даты
#     # при необходимости сервер создает и отправляет новый список

#     print(reminder)
#     return {"detail": "success"}


# @router.patch(
#     "/reminders",
#     tags=['From TG'],
#     summary="Move the date forward one hour/day (PATCH)"
# )
# async def shift_reminder():
#     """ Move the date forward one hour/day """

#     return {"detail": "success"}


# @router.post(
#     "/reminders-list",
#     tags=['From Server'],
#     summary="Getting new reminders list and date"
# )
# async def set_reminder_list():
#     """ Create new reminders list and date from the main server """

#     return {"detail": "success"}


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
async def test_dajngo_post():  # тестовая передача запроса от TG в backend
    """  """

    await send_test_to_Django('data')
    print('Получен post запрос от TG')
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
