from datetime import datetime, date, time
from typing import Optional
import pytz
from django.utils import timezone as django_timezone


def convert_user_datetime_to_utc(
    user_date: date,
    user_time: time,
    user_timezone_str: Optional[str]
) -> tuple[date, time]:
    """
    Конвертирует дату и время из часового пояса пользователя в UTC.
    
    Args:
        user_date: Дата в часовом поясе пользователя
        user_time: Время в часовом поясе пользователя
        user_timezone_str: Строка часового пояса пользователя (например, 'Europe/Samara')
    
    Returns:
        tuple[date, time]: Дата и время в UTC
    """
    if not user_timezone_str:
        # Если часовой пояс не указан, считаем что данные уже в UTC
        return user_date, user_time
    
    try:
        user_tz = pytz.timezone(user_timezone_str)
    except pytz.exceptions.UnknownTimeZoneError:
        # Если часовой пояс неизвестен, считаем что данные уже в UTC
        return user_date, user_time
    
    # Создаем datetime без указания часового пояса
    user_datetime = datetime.combine(user_date, user_time)
    # Соединяем datetime и часовой пояс
    user_datetime = user_tz.localize(user_datetime)
    # Конвертируем в UTC
    utc_datetime = user_datetime.astimezone(pytz.UTC)
    
    return utc_datetime.date(), utc_datetime.time()


def convert_utc_datetime_to_user(
    utc_date: date,
    utc_time: time,
    user_timezone_str: Optional[str]
) -> tuple[date, time]:
    """
    Конвертирует дату и время из UTC в часовой пояс пользователя.
    
    Args:
        utc_date: Дата в UTC
        utc_time: Время в UTC
        user_timezone_str: Строка часового пояса пользователя (например, 'Europe/Samara')
    
    Returns:
        tuple[date, time]: Дата и время в часовом поясе пользователя
    """
    if not user_timezone_str:
        # Если часовой пояс не указан, возвращаем как есть
        return utc_date, utc_time
    
    try:
        user_tz = pytz.timezone(user_timezone_str)
    except pytz.exceptions.UnknownTimeZoneError:
        # Если часовой пояс неизвестен, возвращаем как есть
        return utc_date, utc_time
    
    # Создаем datetime без указания часового пояса
    utc_datetime = datetime.combine(utc_date, utc_time)
    # Соединяем datetime и UTC
    utc_datetime = pytz.UTC.localize(utc_datetime)
    # Конвертируем в часовой пояс пользователя
    user_datetime = utc_datetime.astimezone(user_tz)
    
    return user_datetime.date(), user_datetime.time()


def get_user_now_datetime(user_timezone_str: Optional[str]) -> datetime:
    """
    Получает текущее время в часовом поясе пользователя.
    
    Args:
        user_timezone_str: Строка часового пояса пользователя
    
    Returns:
        datetime: Текущее время в часовом поясе пользователя (без timezone info)
    """
    if not user_timezone_str:
        # Если часовой пояс не указан, возвращаем UTC
        return django_timezone.now().replace(tzinfo=None)
    
    try:
        user_tz = pytz.timezone(user_timezone_str)
    except pytz.exceptions.UnknownTimeZoneError:
        # Если часовой пояс неизвестен, возвращаем UTC
        return django_timezone.now().replace(tzinfo=None)
    
    # Получаем текущее время в UTC
    utc_now = django_timezone.now()
    # Конвертируем в часовой пояс пользователя
    user_now = utc_now.astimezone(user_tz)
    
    return user_now.replace(tzinfo=None)
