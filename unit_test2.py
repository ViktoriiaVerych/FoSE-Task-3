import unittest
from unittest.mock import patch, Mock
import data_processing
import datetime

class TestGetUserData(unittest.TestCase):
    def setUp(self):
        self.date = datetime.datetime.now()
        self.mock_load_data = patch('data_processing.load_data').start()
        self.test_user_id = 'test_user'
        self.invalid_user_id = 'invalid_user'
        self.user = {'userId': self.test_user_id, 'isOnline': True, 'onlinePeriods': [['2023-09-25T17:26:28.123456+03:00', None]]}
        self.mock_load_data.return_value = [self.user]

    def tearDown(self):
        self.mock_load_data.stop()

    def test_valid_date(self):
        result = data_processing.get_user_data(self.date, self.test_user_id)
        self.assertEqual(result['wasUserOnline'], True)
        self.assertIsNone(result['nearestOnlineTime'])

    def test_invalid_user(self):
        result = data_processing.get_user_data(self.date, self.invalid_user_id)
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()
