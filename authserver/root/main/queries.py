import requests

from root.settings import PROJECT_HOSTS


def create_root_folders(user_id):
    """Signal for creating roots after registration"""

    try:
        url = PROJECT_HOSTS['backend'] + "api/auth/create-roots/"
        headers = {
            'Content-Type': 'application/json'
        }

        data = {'user_id': user_id}
        response = requests.post(
            url, json=data, headers=headers, timeout=10
        )

        if response.status_code == 201:
            return True
        else:
            return False

    except requests.exceptions.RequestException:
        # Недоступность сервера - ConnectionError
        # Превышение таймаута (5 секунд)
        # Превышение редиректов - TooManyRedirects
        # Ошибки сети
        # HTTP-ошибки (4xx, 5xx) - HTTPError
        return False
    except Exception:
        return False
