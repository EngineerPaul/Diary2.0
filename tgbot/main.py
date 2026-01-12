from telebot import TeleBot

from config import TOKEN, DEBUG, MY_ID
from api.bot.routers import command_registry
from utils import check_connection


check_connection()

BOT = TeleBot(TOKEN)

if __name__ == '__main__':
    command_registry(BOT)
    if DEBUG:
        BOT.send_message(MY_ID, 'Бот запущен')

    BOT.infinity_polling()
