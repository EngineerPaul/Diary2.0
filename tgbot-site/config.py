from dotenv import load_dotenv
import os


load_dotenv()  # загрузка переменных .env в переменные окружения сессии

TOKEN = os.getenv('TOKEN')
DEBUG = os.getenv('DEBUG')
MY_ID = os.getenv('ID')
SITELINK = os.getenv('SITELINK')
MAX_YEAR = 5
