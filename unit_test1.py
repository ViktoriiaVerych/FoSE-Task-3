import unittest
from unittest.mock import patch, Mock
import data_processing  

class TestGetData(unittest.TestCase):
    @patch('data_processing.requests.get')
    def test_valid_offset(self, mock_get):
        expected_data = {'data': 'test_data'}
        mock_response = Mock()
        mock_response.json.return_value = expected_data
        mock_get.return_value = mock_response

        result = data_processing.get_data(0)

        self.assertEqual(result, expected_data['data'])

class TestUpdateUserData(unittest.TestCase):
    def test_valid_user_prev(self):
        user = {'userId': 'test_user', 'isOnline': True}
        previous_state = {'test_user': {'userId': 'test_user', 'isOnline': False, 'onlinePeriods': []}}

        result = data_processing.update_user_data(user, previous_state)

        self.assertEqual(result['userId'], 'test_user')
        self.assertEqual(result['isOnline'], True)
        self.assertEqual(len(result['onlinePeriods']), 1)

if __name__ == "__main__":
    unittest.main()
