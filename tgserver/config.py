from dotenv import load_dotenv
import os
import json


load_dotenv()  # загрузка переменных .env в переменные окружения сессии

TG_TOKEN = os.getenv('TGTOKEN')
MY_TG_ID = os.getenv('MY_TG_ID')

redis_host = os.getenv("REDIS_HOST")
redis_port = int(os.getenv("REDIS_PORT"))
redis_username = os.getenv("REDIS_USER")
redis_user_password = os.getenv("REDIS_USER_PASSWORD")

PROJECT_HOSTS = json.loads(os.getenv('PROJECT_HOSTS'))
