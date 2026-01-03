from django.test import Client, TestCase


class TestOfTestDateAPI(TestCase):
    path = '/api/periodic-date/'

    def setUp(self) -> None:
        self.client = Client()

    def test_test(self):
        response = self.client.get('/api/public/')
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
