import requests

from root.settings import PROJECT_HOSTS


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
