from datetime import datetime

from main.models import Notice

NOTICE_TITLE_MAX_LENGTH = 50


def telegram_notice_title_placeholder(created_at: datetime) -> str:
    """Заголовок-заглушка для длинного текста из Telegram (дата — в TZ пользователя)."""
    date_part = (
        f'{created_at.day:02d}.{created_at.month:02d}.'
        f'{str(created_at.year)[-2:]}'
    )
    return f'telegram напоминание от {date_part}'


def split_telegram_notice_text(
    msg_text: str, msg_datetime: datetime
) -> tuple[str, str | None]:
    """Короткий текст — в title, длинный — в description с автозаголовком."""
    if len(msg_text) <= NOTICE_TITLE_MAX_LENGTH:
        return msg_text, None
    return telegram_notice_title_placeholder(msg_datetime), msg_text


def notice_delivery_text(notice: Notice) -> str:
    """Текст для отправки напоминания в Telegram."""
    if notice.description:
        return notice.description
    return notice.title
