import re
from datetime import datetime

FULL_DATETIME = re.compile(
    r'^(\d{1,2})\.(\d{1,2})\.(\d{4})\s+(\d{1,2})[.:](\d{2})$'
)
DATE_ONLY = re.compile(r'^(\d{1,2})\.(\d{1,2})\.(\d{4})$')
DAY_MONTH_TIME = re.compile(r'^(\d{1,2})\.(\d{1,2})\s+(\d{1,2})[.:](\d{2})$')
DAY_TIME = re.compile(r'^(\d{1,2})\s+(\d{1,2})[.:](\d{2})$')
DAY_HOUR = re.compile(r'^(\d{1,2})\s+(\d{1,2})$')
TIME_ONLY = re.compile(r'^(\d{1,2})[.:](\d{2})$')
HOUR_ONLY = re.compile(r'^(\d{1,2})$')


def _format_reminder_date(day: int, month: int, year: int, hour: int, minute: int) -> str:
    """Return date string in the format expected by get_date: ДД.ММ.ГГГГ ЧЧ.ММ."""
    return f'{day:02d}.{month:02d}.{year} {hour:02d}.{minute:02d}'


def normalize_reminder_date_input(text: str, now: datetime | None = None) -> str | None:
    """Parse flexible reminder date input and normalize to ДД.ММ.ГГГГ ЧЧ.ММ.

    Supported formats:
    - ДД.ММ.ГГГГ ЧЧ:ММ (or ЧЧ.ММ)
    - ДД.ММ ЧЧ:ММ — current year
    - ДД ЧЧ:ММ — current month and year
    - ЧЧ:ММ — today
    - ЧЧ — today at the given hour, 0 minutes
    - ДД.ММ.ГГГГ — current time
    """
    text = text.strip()
    if not text:
        return None

    reference = now or datetime.now()

    if match := FULL_DATETIME.match(text):
        day, month, year, hour, minute = map(int, match.groups())
        return _format_reminder_date(day, month, year, hour, minute)

    if match := DATE_ONLY.match(text):
        day, month, year = map(int, match.groups())
        return _format_reminder_date(
            day, month, year, reference.hour, reference.minute
        )

    if match := DAY_MONTH_TIME.match(text):
        day, month, hour, minute = map(int, match.groups())
        return _format_reminder_date(day, month, reference.year, hour, minute)

    if match := DAY_TIME.match(text):
        day, hour, minute = map(int, match.groups())
        return _format_reminder_date(
            day, reference.month, reference.year, hour, minute
        )

    if match := DAY_HOUR.match(text):
        day, hour = map(int, match.groups())
        return _format_reminder_date(
            day, reference.month, reference.year, hour, 0
        )

    if match := TIME_ONLY.match(text):
        hour, minute = map(int, match.groups())
        return _format_reminder_date(
            reference.day, reference.month, reference.year, hour, minute
        )

    if match := HOUR_ONLY.match(text):
        hour = int(match.group(1))
        return _format_reminder_date(
            reference.day, reference.month, reference.year, hour, 0
        )

    return None
