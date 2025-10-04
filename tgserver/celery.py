from mongo import upcoming_reminders, upcoming_date
from queries_tg import send_msg_bot


async def check_upcoming():
    # проверка совпадения даты для отправки списка сообщений
    if upcoming_date == 'now':
        await send_all_reminders()


async def send_all_reminders():
    # отправить все сообщения из списка
    for rem in upcoming_reminders:
        await send_msg_bot(
            chat_id=rem.tg_id,
            text=rem.message,
            user_id=rem.user_id,
            reminder_id=rem.reminder_id,
        )
        print('Сообщение отправлено')
