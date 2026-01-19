from utils.secrets import get_secret, get_json_secret

TG_TOKEN = get_secret('TGTOKEN')
MY_TG_ID = get_secret('MY_TG_ID')

REDIS_WORKS = get_json_secret('REDIS_WORKS', [])
redis_host = get_secret("REDIS_HOST")
redis_port = int(get_secret("REDIS_PORT", "6379"))
redis_username = get_secret("REDIS_USER")
redis_user_password = get_secret("REDIS_USER_PASSWORD")

PROJECT_HOSTS = get_json_secret('PROJECT_HOSTS', [])
