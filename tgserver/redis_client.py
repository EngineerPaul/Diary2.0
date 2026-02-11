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
    """ Saving variable in the redis """

    json_var = json.dumps(var)
    if (not json_var):
        return "The variable isn't serialized to JSON"
    if type(key) is not str:
        return "The key must be of str type"
    redis_client.set(key, json_var)
    return True


def redis_get(key):
    """ Getting variable from the redis """

    var = redis_client.get(key)
    response = None if var is None else json.loads(var)
    return response


def redis_del(key):
    """ Removing variable from the redis """

    response = redis_client.delete(key)
    return response
