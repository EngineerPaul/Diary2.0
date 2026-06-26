from datetime import datetime
from types import SimpleNamespace

from django.test import Client, SimpleTestCase, TestCase

from main.utils.tg_notice_content import (
    NOTICE_TITLE_MAX_LENGTH,
    notice_delivery_text,
    split_telegram_notice_text,
    telegram_notice_title_placeholder,
)


class TestOfTestDateAPI(TestCase):
    path = '/api/tests/periodic-date/'

    def setUp(self) -> None:
        self.client = Client()

    def test_test(self):
        response = self.client.get('/api/tests/public/')
        self.assertEqual(response.status_code, 200)

    def test_D_1(self):
        body = {
            'initial_date': '2025-12-25',
            'period': '10,0,0,0',
            'time': '19:00'
        }
        response = self.client.post(path=self.path, data=body)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['next_date'], '2026-01-04')

    def test_DW_1(self):
        body = {
            'initial_date': '2025-12-25',
            'period': '5,1,0,0',
            'time': '19:00'
        }
        response = self.client.post(path=self.path, data=body)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['next_date'], '2025-12-26')

    def test_DW_2(self):
        body = {
            'initial_date': '2025-12-25',
            'period': '4,2,0,0',
            'time': '00:00'
        }
        response = self.client.post(path=self.path, data=body)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['next_date'], '2026-01-08')

    def test_DW_3(self):
        body = {
            'initial_date': '2025-12-25',
            'period': '4,2,0,0',
            'time': '23:59'
        }
        response = self.client.post(path=self.path, data=body)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['next_date'], '2025-12-25')

    def test_DWM_1(self):
        body = {
            'initial_date': '2025-12-25',
            'period': '5,4,1,0',
            'time': '19:00'
        }
        response = self.client.post(path=self.path, data=body)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['next_date'], '2025-12-26')

    def test_DWM_2(self):
        body = {
            'initial_date': '2025-12-25',
            'period': '5,5,1,0',
            'time': '19:00'
        }
        response = self.client.post(path=self.path, data=body)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['next_date'], '2025-12-26')

    def test_DWM_3(self):
        body = {
            'initial_date': '2025-12-25',
            'period': '2,2,2,0',
            'time': '19:00'
        }
        response = self.client.post(path=self.path, data=body)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['next_date'], '2026-02-03')

    def test_DWM_4(self):
        # в месяце 5 недель, а просим 6 (возвращает 5)
        body = {
            'initial_date': '2025-12-25',
            'period': '1,6,1,0',
            'time': '19:00'
        }
        response = self.client.post(path=self.path, data=body)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['next_date'], '2025-12-29')

    def test_DM_1(self):
        body = {
            'initial_date': '2025-12-25',
            'period': '26,0,2,0',
            'time': '19:00'
        }
        response = self.client.post(path=self.path, data=body)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['next_date'], '2025-12-26')

    def test_DM_2(self):
        body = {
            'initial_date': '2025-12-25',
            'period': '10,0,2,0',
            'time': '19:00'
        }
        response = self.client.post(path=self.path, data=body)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['next_date'], '2026-02-10')

    def test_DM_3(self):
        body = {
            'initial_date': '2026-02-01',
            'period': '31,0,2,0',
            'time': '19:00'
        }
        response = self.client.post(path=self.path, data=body)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['next_date'], '2026-02-28')

    def test_DY_1(self):
        body = {
            'initial_date': '2025-12-25',
            'period': '365,0,0,1',
            'time': '19:00'
        }
        response = self.client.post(path=self.path, data=body)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['next_date'], '2025-12-31')

    def test_DY_2(self):
        body = {
            'initial_date': '2025-12-25',
            'period': '30,0,0,1',
            'time': '19:00'
        }
        response = self.client.post(path=self.path, data=body)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['next_date'], '2026-01-30')

    def test_DY_3(self):
        body = {
            'initial_date': '2025-12-25',
            'period': '32,0,0,1',
            'time': '19:00'
        }
        response = self.client.post(path=self.path, data=body)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['next_date'], '2026-02-01')

    def test_DWY_1(self):
        body = {
            'initial_date': '2025-12-25',
            'period': '5,1,0,1',
            'time': '19:00'
        }
        response = self.client.post(path=self.path, data=body)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['next_date'], '2026-01-02')

    def test_DWY_2(self):
        body = {
            'initial_date': '2025-12-25',
            'period': '1,52,0,1',
            'time': '19:00'
        }
        response = self.client.post(path=self.path, data=body)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['next_date'], '2025-12-29')

    def test_DWMY_1(self):
        body = {
            'initial_date': '2025-12-25',
            'period': '1,5,12,1',
            'time': '19:00'
        }
        response = self.client.post(path=self.path, data=body)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['next_date'], '2025-12-29')

    def test_DWMY_2(self):
        body = {
            'initial_date': '2025-12-25',
            'period': '5,2,1,1',
            'time': '19:00'
        }
        response = self.client.post(path=self.path, data=body)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['next_date'], '2026-01-09')

    def test_DWMY_3(self):
        body = {
            'initial_date': '2025-12-25',
            'period': '5,2,2,1',
            'time': '19:00'
        }
        response = self.client.post(path=self.path, data=body)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['next_date'], '2026-02-06')

    def test_DMY_1(self):
        body = {
            'initial_date': '2025-12-25',
            'period': '10,0,1,1',
            'time': '19:00'
        }
        response = self.client.post(path=self.path, data=body)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['next_date'], '2026-01-10')

    def test_DMY_2(self):
        body = {
            'initial_date': '2025-12-25',
            'period': '31,0,2,1',
            'time': '19:00'
        }
        response = self.client.post(path=self.path, data=body)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['next_date'], '2026-02-28')

    def test_DMY_3(self):
        body = {
            'initial_date': '2025-12-25',
            'period': '29,0,12,1',
            'time': '19:00'
        }
        response = self.client.post(path=self.path, data=body)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['next_date'], '2025-12-29')


class TestTelegramNoticeContent(SimpleTestCase):
    """Тесты для функции split_telegram_notice_text"""
    # SimpleTestCase не создает БД, в отличии от TestCase

    def test_short_text_stays_in_title(self):
        title, desc = split_telegram_notice_text('еда', datetime(2026, 6, 26, 12, 0))
        self.assertEqual(title, 'еда')
        self.assertIsNone(desc)

    def test_exactly_max_length_stays_in_title(self):
        text = 'а' * NOTICE_TITLE_MAX_LENGTH
        title, desc = split_telegram_notice_text(text, datetime(2026, 6, 26))
        self.assertEqual(title, text)
        self.assertIsNone(desc)

    def test_long_text_goes_to_description(self):
        user_text = 'а' * (NOTICE_TITLE_MAX_LENGTH + 1)
        msg_datetime = datetime(2026, 6, 26, 15, 30)
        title, desc = split_telegram_notice_text(user_text, msg_datetime)
        self.assertEqual(title, 'telegram напоминание от 26.06.26')
        self.assertEqual(desc, user_text)
        self.assertLessEqual(len(title), NOTICE_TITLE_MAX_LENGTH)

    def test_placeholder_format(self):
        self.assertEqual(
            telegram_notice_title_placeholder(datetime(2026, 6, 26)),
            'telegram напоминание от 26.06.26',
        )

    def test_delivery_text_prefers_description(self):
        notice = SimpleNamespace(
            title='telegram напоминание от 26.06.26',
            description='Длинный текст',
        )
        self.assertEqual(notice_delivery_text(notice), 'Длинный текст')

    def test_delivery_text_falls_back_to_title(self):
        notice = SimpleNamespace(title='еда', description=None)
        self.assertEqual(notice_delivery_text(notice), 'еда')
