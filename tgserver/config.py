from dotenv import load_dotenv
import os


load_dotenv()  # загрузка переменных .env в переменные окружения сессии

TG_TOKEN = os.getenv('TGTOKEN')
MY_TG_ID = os.getenv('MY_TG_ID')
