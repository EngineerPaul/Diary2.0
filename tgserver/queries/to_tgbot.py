from telebot import TeleBot
from config import TG_TOKEN
from utils.utils import get_markup


BOT = TeleBot(TG_TOKEN)


async def send_msg_bot(chat_id, text, user_id, reminder_id):
    """ Send message in the TG chat """
    # @router.post("/test-send")

    user_id = user_id
    markup = get_markup(
        user_id=user_id,
        reminder_id=reminder_id
    )

    BOT.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode='html',  # режим разметки сообщения
        reply_markup=markup  # прикрепляем кнопки
    )
