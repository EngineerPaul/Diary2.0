from typing import List, Tuple, Dict, Any, Optional, Union
import requests
from django.db.models.functions import Cast, Concat
from django.db.models import DateTimeField, Value
from django.utils import timezone
from datetime import datetime
from django.db.models import Min

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


class UpcomingNoticeList:
    """ Send next notice list to telegram server """

    def main(self, new_date: Optional[datetime] = None) -> bool:
        next_notices, min_datetime = self.get_next_notice_list()
        if not next_notices:
            return False

        if new_date and new_date > min_datetime:  # создание напоминания
            return False  # проверяем, что новая дата не ближайшая

        chat_ids = self.get_chat_ids(next_notices)
        if not chat_ids:
            return False

        next_notices_map = self.mapping_notices_chat_ids(next_notices, chat_ids)

        success = self.send_notice_list(next_notices_map, min_datetime)
        return success

    def get_next_notice_list(self) -> Tuple[List[Notice], Optional[datetime]]:
        """ Get next notice list from database """

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
        return next_notices, min_datetime

    def get_chat_ids(
        self, next_notices: List[Notice]
    ) -> Optional[List[Dict[str, int]]]:
        """ Get chat ids from database """

        url = PROJECT_HOSTS['auth_server'] + "api/users/chat-ids"
        headers = {
            'Content-Type': 'application/json'
        }

        data = {'user_ids': list(next_notices.values_list('user_id', flat=True))}
        response = requests.post(
            url, json=data, headers=headers, timeout=15
        )

        chat_ids = response.json() if response.status_code == 200 else None
        return chat_ids

    def mapping_notices_chat_ids(
        self, next_notices: List[Notice], chat_ids: List[Dict[str, int]]
    ) -> List[Dict[str, Any]]:
        """ Mapping notice info and chat ids """

        # Создаем словарь user_id -> chat_id для быстрого доступа
        user_chat_map = {
            item['user_id']: item['chat_id']
            for item in chat_ids
        }

        # Фильтруем next_notices и добавляем chat_id
        notices_with_chat = []
        for notice in next_notices:
            chat_id = user_chat_map.get(notice.user_id)
            if chat_id:  # Только если есть chat_id
                notice_data = {
                    'user_id': notice.user_id,
                    'text': notice.title,
                    'reminder_id': notice.id,
                    'chat_id': chat_id
                }
                notices_with_chat.append(notice_data)

        return notices_with_chat

    def send_notice_list(
        self, notices_with_chat: List[Dict[str, Any]], min_datetime: datetime
    ) -> Union[bool, requests.Response]:
        """ Send notice list to telegram server """

        url = PROJECT_HOSTS['tg_server'] + "tgapi/set-notice-list/"
        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            'notice_list': notices_with_chat,
            #   {'user_id': notice.user_id,
            #   'text': notice.title,
            #   'reminder_id': notice.id,
            #   'chat_id': chat_id}
            'next_date': min_datetime
        }
        respone = requests.post(
            url, json=data, headers=headers, timeout=15
        )
        if respone.status_code != 200:
            return False
        return respone


def get_user_id(chat_id: int) -> int:
    """ Get user_id by tg chat_id from auth server """

    try:
        url = PROJECT_HOSTS['auth_server'] + "api/users/user-id/"
        headers = {
            'Content-Type': 'application/json'
        }

        data = {'chat_id': chat_id}
        response = requests.post(
            url, json=data, headers=headers, timeout=15
        )
        if response.status_code != 200:
            return False

        return response.json()

    except (requests.exceptions.RequestException, Exception):
        return False
