from fastapi import APIRouter
from schemas import ReminderCreater
from queries_tg import send_msg_bot
from config import MY_TG_ID


router = APIRouter()

@router.post("/reminders")
async def create_reminder(reminder: ReminderCreater):
    print(reminder)
    return {"detail": "success"}


@router.patch("/reminders")
async def shift_reminder():
    return {"detail": "success"}


@router.post("/reminders-list")
async def get_reminder_list():
    return {"detail": "success"}


@router.post("/test-send")
async def test_query():

    await send_msg_bot(
        chat_id=MY_TG_ID,
        text='Какой-то текст из API',
        user_id=100,
        reminder_id=100
    )

    return {"detail": "success"}


@router.post("/test-celery")
async def test_celery():
    from celery import check_upcoming

    print("check_upcoming запущен")
    await check_upcoming()
    return {"detail": "success"}
