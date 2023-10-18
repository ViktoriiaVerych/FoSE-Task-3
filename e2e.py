import os
from flask import Flask
from flask.testing import FlaskClient
import pytest
from unittest.mock import patch

BASE_URL = os.getenv('BASE_URL', 'http://176.36.23.13')

app = Flask(__name__)
client = app.test_client()

@app.route('/api/stats/user/online_time', methods=['GET'])
def get_online_time():
    user = {'userId': '1', 'onlinePeriods': [['2023-11-14T13:21:54', None]]}
    previous_state = {}
    mock_update_user_data.return_value = user, previous_state
    mock_calculate_online_time.return_value = 1000

    userId = '1'
    response = client.get(f'/api/stats/user/online_time?userId={userId}')

    assert response.status_code == 200
    data = response.json
    assert 'onlineTime' in data
    assert data['onlineTime'] == 1000

if __name__ == "__main__":
    pytest.main()
client = app.test_client()

if __name__ == "__main__":
    pytest.main()