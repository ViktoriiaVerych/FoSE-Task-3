import pytest
from datetime import datetime, timedelta
from data_procession import predict_user

class TestPredictUser:
    def test_online_user(self, mocker):
        mocker.patch('builtins.open', new_callable=mock_open, read_data='[{"userId": 1, "isOnline": true, "lastSeenDate": "2023-10-05T18:38:28", "onlinePeriods": [["2023-10-05T18:38:28", null]]}]')
        date = datetime.utcnow()
        result = predict_user(date, 1, 0.5)
        assert result['willBeOnline'] == True
        assert result['onlineChance'] == 1

    def test_offline_user(self, mocker):
        mocker.patch('builtins.open', new_callable=mock_open, read_data='[{"userId": 1, "isOnline": false, "lastSeenDate": "2023-10-05T18:38:28", "onlinePeriods": [["2023-10-05T18:38:28", "2023-10-05T19:38:28"]]}]')
        date = datetime.utcnow() + timedelta(hours=2)
        result = predict_user(date, 1, 0.5)
        assert result['willBeOnline'] == False
        assert result['onlineChance'] == 0

    def test_online_user_and_low_tol(self, mocker):
        mocker.patch('builtins.open', new_callable=mock_open, read_data='[{"userId": 1, "isOnline": true, "lastSeenDate": "2023-10-05T18:38:28", "onlinePeriods": [["2023-10-05T18:38:28", null]]}]')
        date = datetime.utcnow()
        result = predict_user(date, 1, 0.1)
        assert result['willBeOnline'] == True
        assert result['onlineChance'] == 1

    def test_offline_user_and_high_tol(self, mocker):
        mocker.patch('builtins.open', new_callable=mock_open, read_data='[{"userId": 1, "isOnline": false, "lastSeenDate": "2023-10-05T18:38:28", "onlinePeriods": [["2023-10-05T18:38:28", "2023-10-05T19:38:28"]]}]')
        date = datetime.utcnow() + timedelta(hours=2)
        result = predict_user(date, 1, 0.9)
        assert result['willBeOnline'] == True
        assert result['onlineChance'] == 0.5

if __name__ == "__main__":
    pytest.main()
    unittest.main()
