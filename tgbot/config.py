from utils.secrets import get_secret, get_json_secret


# Получаем секреты через unified secrets module
TOKEN = get_secret('TOKEN')
DEBUG = get_secret('DEBUG')
MY_ID = get_secret('ID')
SITELINK = get_secret('SITELINK')
# MAX_YEAR = get_secret('MAX_YEAR', '5')  # Значение по умолчанию как строка
MAX_YEAR = 5
PROJECT_HOSTS = get_json_secret('PROJECT_HOSTS')
