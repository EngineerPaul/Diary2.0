from dotenv import load_dotenv
import os
import json


load_dotenv()  # загрузка переменных .env в переменные окружения сессии

TOKEN = os.getenv('TOKEN')
DEBUG = os.getenv('DEBUG')
MY_ID = os.getenv('ID')
SITELINK = os.getenv('SITELINK')
MAX_YEAR = 5
PROJECT_HOSTS = json.loads(os.getenv('PROJECT_HOSTS'))
