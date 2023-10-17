import unittest
from unittest.mock import patch
from datetime import datetime, timedelta
import data_procession as dp

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.mock_get_patcher = patch('dp.requests.get')
        self.mock_get = self.mock_get_patcher.start()
        self.mock_resp = self.mock_get.return_value
        self.mock_resp.json.return_value = {'data': [{'userId': '1', 'isOnline': True, 'lastSeenDate': '2023-10-06T08:35:30'}]}
        dp.fetch_and_update_data()

    def tearDown(self):
        self.mock_get_patcher.stop()

    def test_UpdateData_When_UserStatusChanges(self):
        self.assertEqual(len(dp.get_previous_state()), 1)

        self.mock_resp.json.return_value = {'data': [{'userId': '1', 'isOnline': False, 'lastSeenDate': '2023-10-06T08:35:30'}]}

        dp.fetch_and_update_data()
        self.assertEqual(dp.get_previous_state()['1']['isOnline'], False)

    def test_ReturnUsersOnline_When_GetDataWithValidOffset(self):
        self.assertEqual(len(dp.get_previous_state()), 1)

        fixed_dt = datetime(2023, 10, 6, 8, 35, 30)
        users_online = dp.get_users_online(fixed_dt)
        self.assertEqual(users_online, 1)

    def test_ReturnWillBeOnline_When_PredictUserWithValidData(self):
        self.assertEqual(len(dp.get_previous_state()), 1)

        user_pred = dp.predict_user(datetime.now(), '1', 0.5)
        self.assertIsNotNone(user_pred)
        self.assertIn('willBeOnline', user_pred)

    def test_ReturnOnlineChance_When_PredictUserWithValidData(self):
        self.assertEqual(len(dp.get_previous_state()), 1)

        user_pred = dp.predict_user(datetime.now(), '1', 0.5)
        self.assertIsNotNone(user_pred)
        self.assertIn('onlineChance', user_pred)

    def test_ReturnUsersOnlinePrediction_When_GetDataWithValidOffset(self):
        user_data = dp.get_user_data(datetime.now(), '1')
        self.assertTrue(user_data['wasUserOnline'])

        prediction = dp.predict_users(datetime.now())
        self.assertEqual(prediction['onlineUsers'], 1)

if __name__ == '__main__':
    unittest.main()
