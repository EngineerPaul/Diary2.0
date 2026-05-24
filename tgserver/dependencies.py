import aiohttp
from fastapi import Depends, Header, HTTPException

from config import INTERNAL_SERVICE_TOKEN
from utils.service_auth import SERVICE_TOKEN_HEADER


_session: aiohttp.ClientSession | None = None


async def verify_service_token(
    x_service_token: str | None = Header(default=None, alias=SERVICE_TOKEN_HEADER),
) -> None:
    if not INTERNAL_SERVICE_TOKEN or x_service_token != INTERNAL_SERVICE_TOKEN:
        raise HTTPException(status_code=403, detail='Forbidden')


async def get_session() -> aiohttp.ClientSession:
    """ Вызов сессии для отправки запросов.
    Сессия создается один раз при запуске приложения """
    if _session is None:
        raise RuntimeError("ClientSession не инициализирован. Проверьте startup-событие.")
    return _session

async def set_session():
    """ Создание сессии (при запуске приложения) """
    global _session
    _session = aiohttp.ClientSession()
    return _session

async def close_session():
    """ Закрытие сессии (при отключении приложения) """
    if _session:
        await _session.close()
