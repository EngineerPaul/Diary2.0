import redis
import json

from config import redis_host, redis_port, redis_username, redis_user_password


redis_client = redis.Redis(
    host=redis_host,  # при запуске через контейнер испю название контейнера
    port=redis_port,  # при запуске через контейнер работает без мапинга
    db=0,  # в redis по умолчанию 16 баз данных (0-15)
    username=redis_username,
    password=redis_user_password,
    decode_responses=True  # декодирует байтовые ответы redis в python форматы
)


def redis_set(key, var):
    json_var = json.dumps(var)
    if (not json_var):
        return "The variable isn't serialized to JSON"
    if type(key) != str:
        return "The key must be of str type"
    redis_client.set(key, json_var)
    return True


def redis_get(key):
    var = redis_client.get(key)
    if var == None:
        return f"The {key} key doens't exist"
    var = json.loads(var)
    return var


def redis_del(key):
    response = redis_client.delete(key)
    return response
