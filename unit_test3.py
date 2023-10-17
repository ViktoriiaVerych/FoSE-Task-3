import unittest
from unittest.mock import patch, Mock
import data_processing
import datetime

class TestPredictUsers(unittest.TestCase):
    def setUp(self):
        self.user = {'userId': 'test_user', 'isOnline': True, 'onlinePeriods': [['2023-09-25T17:26:28.123456+03:00', None]]}
        self.mock_load_data = patch('data_processing.load_data').start()
        self.mock_load_data.return_value = [self.user]

    def tearDown(self):
        patch.stopall()

    def test_predict_with_valid_date(self):
        with patch('datetime.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime.datetime(2023, 9, 25, 17, 26, 28, 123456)
            date = datetime.datetime.now()

            result = data_processing.predict_users(date)

            self.assertEqual(result['onlineUsers'], 1)

if __name__ == "__main__":
    unittest.main()
