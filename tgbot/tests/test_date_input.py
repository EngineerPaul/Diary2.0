from datetime import datetime, timedelta
from unittest.mock import patch

import pytest

from utils.date_input import normalize_reminder_date_input
from utils.utils import get_date


NOW = datetime(2030, 1, 15, 14, 30)  # 15.01.2030 14:30


@pytest.mark.parametrize(
    ('raw', 'expected'),
    [
        ('16.02.2031 09:00', '16.02.2031 09.00'),
        ('16.02.2031 09.00', '16.02.2031 09.00'),
        ('16.02.2031', '16.02.2031 14.30'),
        ('16.02 09:00', '16.02.2030 09.00'),
        ('16.02 09.00', '16.02.2030 09.00'),
        ('20 09:00', '20.01.2030 09.00'),
        ('20 09.00', '20.01.2030 09.00'),
        ('20 9', '20.01.2030 09.00'),
        ('09:00', '15.01.2030 09.00'),
        ('9.00', '15.01.2030 09.00'),
        ('18', '15.01.2030 18.00'),
        ('  16.02 09:00  ', '16.02.2030 09.00'),
    ],
)
def test_normalize_reminder_date_input(raw, expected):
    assert normalize_reminder_date_input(raw, now=NOW) == expected


@pytest.mark.parametrize('raw', ['', 'bad', '16-02 09:00'])
def test_normalize_reminder_date_input_invalid(raw):
    assert normalize_reminder_date_input(raw, now=NOW) is None


def test_normalize_with_get_date_short_formats():
    future_now = datetime.now() + timedelta(days=2)
    normalized = normalize_reminder_date_input(
        f'{future_now.day} 12:00',
        now=future_now,
    )
    result = get_date(normalized)
    assert result['status'] is True
    assert result['details'].day == future_now.day
    assert result['details'].hour == 12
    assert result['details'].minute == 0


def test_normalize_with_get_date_time_only_today():
    fixed_now = datetime(2030, 1, 15, 10, 0, 0)  # 15.01.2030 10:00
    normalized = normalize_reminder_date_input('15:30', now=fixed_now)
    assert normalized == '15.01.2030 15.30'

    with patch('utils.utils.datetime') as mock_dt:
        mock_dt.now.return_value = fixed_now
        mock_dt.side_effect = lambda *args, **kw: datetime(*args, **kw)
        result = get_date(normalized)

    assert result['status'] is True
    assert result['details'].hour == 15
    assert result['details'].minute == 30
