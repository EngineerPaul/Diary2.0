import asyncio
import logging

import aiohttp

from config import PROJECT_HOSTS
from utils.request_context import merge_request_headers

logger = logging.getLogger(__name__)


class APIClient:
    """Клиент для работы с Django API."""

    def __init__(self, base_url):
        self.base_url = base_url
        self.timeout = aiohttp.ClientTimeout(total=10)

    async def _request(self, method, endpoint, json_data=None, params=None):
        """
        Базовый метод для HTTP запросов.

        Args:
            method: HTTP метод ('GET', 'POST', 'PATCH', 'DELETE')
            endpoint: путь API (например, 'tgapi/from-tg-to-django')
            json_data: данные для POST/PATCH запроса (dict)
            params: параметры для GET запроса (dict)

        Returns:
            str: ответ от сервера, или None в случае ошибки
        """
        url = self.base_url + endpoint
        headers = merge_request_headers()

        try:
            async with aiohttp.ClientSession(
                timeout=self.timeout
            ) as session:
                method_upper = method.upper()
                if method_upper == 'POST':
                    async with session.post(
                        url, json=json_data, headers=headers
                    ) as resp:
                        resp.raise_for_status()
                        res = await resp.text()
                        logger.info(
                            'HTTP request completed',
                            extra={'extra_fields': {'method': 'POST', 'endpoint': endpoint, 'status': resp.status}},
                        )
                        return res
                elif method_upper == 'GET':
                    async with session.get(url, params=params, headers=headers) as resp:
                        resp.raise_for_status()
                        res = await resp.text()
                        logger.info(
                            'HTTP request completed',
                            extra={'extra_fields': {'method': 'GET', 'endpoint': endpoint, 'status': resp.status}},
                        )
                        return res
                elif method_upper == 'PATCH':
                    async with session.patch(
                        url, json=json_data, headers=headers
                    ) as resp:
                        resp.raise_for_status()
                        res = await resp.text()
                        logger.info(
                            'HTTP request completed',
                            extra={'extra_fields': {'method': 'PATCH', 'endpoint': endpoint, 'status': resp.status}},
                        )
                        return res
                elif method_upper == 'DELETE':
                    async with session.delete(url, headers=headers) as resp:
                        resp.raise_for_status()
                        res = await resp.text()
                        logger.info(
                            'HTTP request completed',
                            extra={'extra_fields': {'method': 'DELETE', 'endpoint': endpoint, 'status': resp.status}},
                        )
                        return res
        except aiohttp.ClientError as e:
            logger.error(f'HTTP client error: {e}', extra={'extra_fields': {'endpoint': endpoint}})
            return None
        except asyncio.TimeoutError:
            logger.error('HTTP request timeout', extra={'extra_fields': {'endpoint': endpoint}})
            return None
        except Exception as e:
            logger.exception(f'Unexpected HTTP error: {e}', extra={'extra_fields': {'endpoint': endpoint}})
            return None

    def post(self, endpoint, json_data):
        """POST запрос."""
        try:
            async def _post():
                return await self._request('POST', endpoint, json_data)

            return asyncio.run(_post())
        except RuntimeError as e:
            logger.error(f'Event loop error: {e}')
            return None

    def get(self, endpoint, params=None):
        """GET запрос."""
        try:
            async def _get():
                return await self._request('GET', endpoint, params=params)

            return asyncio.run(_get())
        except RuntimeError as e:
            logger.error(f'Event loop error: {e}')
            return None

    def patch(self, endpoint, json_data):
        """PATCH запрос."""
        try:
            async def _patch():
                return await self._request('PATCH', endpoint, json_data)

            return asyncio.run(_patch())
        except RuntimeError as e:
            logger.error(f'Event loop error: {e}')
            return None

    def delete(self, endpoint):
        """DELETE запрос."""
        try:
            async def _delete():
                return await self._request('DELETE', endpoint)

            return asyncio.run(_delete())
        except RuntimeError as e:
            logger.error(f'Event loop error: {e}')
            return None


# Создаем экземпляр клиента на уровне модуля
api_client = APIClient(PROJECT_HOSTS['backend'])
api_tg_client = APIClient(PROJECT_HOSTS['tg_server'])
api_auth_client = APIClient(PROJECT_HOSTS['auth_server'])
