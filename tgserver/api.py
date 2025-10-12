from datetime import datetime, timedelta

from fastapi import APIRouter
from schemas import ReminderCreater
from queries_tg import send_msg_bot
from config import MY_TG_ID
from services import RemindData


router = APIRouter()


@router.post(
    "/reminders",
    tags=['From TG'],
    summary="Create new reminder using the TG bot"
)
async def create_reminder(reminder: ReminderCreater):
    """ Create new reminder using the TG bot """

    # переотправка напоминания на основной сервер
    # сервер сохраняет и проверяет даты
    # при необходимости сервер создает и отправляет новый список

    print(reminder)
    return {"detail": "success"}


@router.patch(
    "/reminders",
    tags=['From TG'],
    summary="Move the date forward one hour/day (PATCH)"
)
async def shift_reminder():
    """ Move the date forward one hour/day """

    return {"detail": "success"}


@router.post(
    "/reminders-list",
    tags=['From Server'],
    summary="Getting new reminders list and date"
)
async def set_reminder_list():
    """ Create new reminders list and date from the main server """

    return {"detail": "success"}


@router.post(
    "/test-send",
    tags=['test'],
    summary="Send test msg to the TG bot"
)
async def test_query():
    """ Quilcky check of sending msg to the TG bot """

    await send_msg_bot(
        chat_id=MY_TG_ID,
        text='Какой-то текст из API',  # можно дополнить любой информацией
        user_id=100,
        reminder_id=100
    )

    return {"detail": "success"}


@router.post(
    "/test-celery-beat",
    tags=['test'],
    summary="Set a test reminder list. Send a msg in 30s"
)
async def test_celery():
    """ Quickly check the work of the reminders list """

    RemindData.set_reminders_list([
        {
            'user_id': 100,
            'reminder_id': 100,
            'message': 'Тестовое напоминание',
            'tg_id': MY_TG_ID,
        },
    ])
    RemindData.set_date(
        datetime.now() + timedelta(seconds=30)
    )

    return {"detail": "success"}
