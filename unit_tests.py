import unittest
from unittest.mock import patch, MagicMock
import data_procession
from datetime import datetime

class TestUserData(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_update_user_data_when_user_is_online_should_update_user_data(self):
        user = {'userId': '1', 'isOnline': True}
        previous_state = {'1': {'userId': '1', 'isOnline': False, 'onlinePeriods': []}}
        updated_user_data = data_procession.update_user_data(user, previous_state)
        self.assertIsNotNone(updated_user_data)
        self.assertEqual(updated_user_data['onlinePeriods'][0][0], expected_value)
        self.assertEqual(updated_user_data['onlinePeriods'][0][1], expected_value)

    def test_update_user_data_when_user_is_offline_should_update_user_data(self):
        user = {'userId': '1', 'isOnline': False}
        previous_state = {'1': {'userId': '1', 'isOnline': True, 'onlinePeriods': [['2023-10-09T11:14:17', None]]}}
        updated_user_data = data_procession.update_user_data(user, previous_state)
        self.assertIsNotNone(updated_user_data)
        self.assertEqual(updated_user_data['onlinePeriods'][0][1], expected_value)

    def test_calculate_online_time_should_return_total_seconds_online(self):
        user = {'userId': '1', 'isOnline': True, 'onlinePeriods': [['2023-10-09T11:14:17', '2023-10-09T11:20:00']]}
        result = data_procession.calculate_online_time(user)
        self.assertEqual(result, 3600)

    def test_calculate_days_should_return_total_days(self):
        user = {'userId': '1', 'isOnline': True, 'onlinePeriods': [['2023-10-09T11:14:17', '2023-10-09T11:20:00']]}
        result = data_procession.calculate_days(user)
        self.assertEqual(result, 2)

    def test_calculate_average_times_should_return_weekly_and_daily_average(self):
        user = {'userId': '1', 'isOnline': True, 'onlinePeriods': [['2023-10-09T11:14:17', '2023-10-09T11:20:00']]}
        weekly_average, daily_average = data_procession.calculate_average_times(user)
        self.assertEqual(weekly_average, 315000.0)
        self.assertEqual(daily_average, 45000.0)

if __name__ == "__main__":
    unittest.main()