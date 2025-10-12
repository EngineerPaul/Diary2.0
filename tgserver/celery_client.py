from celery import Celery
from datetime import timedelta

from config import redis_host, redis_port, redis_username, redis_user_password


# Redis settings
REDIS_HOST = redis_host
REDIS_PORT = redis_port
REDIS_USER = redis_username
REDIS_PASSWORD = redis_user_password

# Celery settings
CELERY_BROKER_URL = f'redis://{REDIS_USER}:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0'
CELERY_RESULT_BACKEND = f'redis://{REDIS_USER}:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0'

celery_app = Celery(
    'celery_app',
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
)
celery_app.conf.imports = (
    'tasks',  # файл с тасками
)


# celery settings
CELERY_BROKER_TRANSPORT_OPTION = {
    'visibility_timeout': 60,  # время жизни сообщения в очереди Redis. По умолчанию 3600сек (1 час)
    'polling_interval': 1,  # интервал опроса очереди в секундах. default=1s
    'max_retries': 3,  # максимальное количество попыток выполнения задачи. default=3
    'interval_start': 0,  # начальный интервал между попытками. default=0
    'interval_step': 1,  # шаг увеличения интервала между попытками
    'connection_timeout': 30,  # время ожидания соединения между воркером и брокером. default=4
    }
CELERY_ACCEPT_CONTENT = {'application': 'json'}
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

celery_app.conf.update(
    broker_transport_option=CELERY_BROKER_TRANSPORT_OPTION,
    task_serializer=CELERY_TASK_SERIALIZER,
    result_serializer=CELERY_RESULT_SERIALIZER,
    accept_content=['json'],
    beat_schedule_filename='beatdata/celerybeat-schedule',
    # расположение системного файла. в dockerfile меняются права
)
# app.conf.update(task_ignore_result=True)  # для отладки

# celery beat settings
celery_app.conf.beat_schedule = {
    # 'my_test_beat': {  # опртавка принта каждые 5с
    #     'task': 'tasks.celery_every_5s',
    #     'schedule': timedelta(seconds=5)
    # },
    'check_dispatch_date': {  # проверка даты оправки каждые 10с
        'task': 'tasks.celery_check_dispatch_date',
        'schedule': timedelta(seconds=10)
    },
}
