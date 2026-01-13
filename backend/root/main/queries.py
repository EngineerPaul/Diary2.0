import requests

from root.settings import PROJECT_HOSTS
from .models import Notice


def test_get():
    """First test send request to telegram server"""

    try:
        url = PROJECT_HOSTS['tg_server'] + "tgapi/test-django/"
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.get(
            url, headers=headers, timeout=15
        )

        print(response)
        print(response.status_code)
        print(response.text)  # текст ответа
        print(response.json())  # JSON ответ (если сервер возвращает JSON)

    except requests.exceptions.RequestException:
        print('RequestException')
        # Недоступность сервера - ConnectionError
        # Превышение таймаута (5 секунд)
        # Превышение редиректов - TooManyRedirects
        # Ошибки сети
        # HTTP-ошибки (4xx, 5xx) - HTTPError
        return False
    except Exception:
        print('Exception')
        return False


def test_post():
    """First test send request to telegram server"""

    try:
        url = PROJECT_HOSTS['tg_server'] + "tgapi/test-django/"
        headers = {
            'Content-Type': 'application/json'
        }

        data = {'msg': 'WORKS!!! Test msg'}
        response = requests.post(
            url, json=data, headers=headers, timeout=15
        )

        print(response)
        print(response.status_code)
        print(response.text)  # текст ответа
        print(response.json())  # JSON ответ (если сервер возвращает JSON)

    except requests.exceptions.RequestException:
        print('RequestException')
        # Недоступность сервера - ConnectionError
        # Превышение таймаута (5 секунд)
        # Превышение редиректов - TooManyRedirects
        # Ошибки сети
        # HTTP-ошибки (4xx, 5xx) - HTTPError
        return False
    except Exception:
        print('Exception')
        return False


def send_notice_list():
    """ Send notice list to telegram server """

    from django.db.models.functions import Cast, Concat
    from django.db.models import DateTimeField, Value
    from django.utils import timezone
    from datetime import datetime
    from django.db.models import Min

    now_date = datetime.now()

    # Получение списка напоминаний c datetime датой
    notices = Notice.objects.annotate(
        full_datetime=Cast(
            Concat('next_date', Value(' '), 'time'),
            output_field=DateTimeField()
        )
    ).filter(full_datetime__gte=timezone.make_aware(now_date))
    # Получение минимального datetime (после now)
    notices = notices.aggregate(
        min_datetime=Min('full_datetime')
    )
    # Результат — словарь: {'min_datetime': datetime.datetime(...)}
    min_datetime = notices['min_datetime']

    next_notices = Notice.objects.filter(
        next_date=min_datetime.date(),
        time=min_datetime.time()
    )
    print(f'{notices.values()=}')
    print(f'{min_datetime=}')
    print(f'{next_notices=}')

    # теперь у нас есть список уведомлений и нужная дата
    # но для FastAPI нужно еще получить chat_id для каждого уведомления

    # print(f'{min_datetime.date()=}')
    # print(f'{min_datetime.time()=}')

    # upcoming_date = Notice.objects.filter(next_date__gte=datetime.now())
    # upcoming_notifications = notices.filter(next_date__gte=datetime.now())
