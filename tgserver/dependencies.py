import aiohttp
from fastapi import Depends


_session: aiohttp.ClientSession | None = None


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