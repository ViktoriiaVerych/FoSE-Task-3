import requests
import json
import time
from datetime import datetime

DATA_FILE = 'all_data.json'
FETCH_INTERVAL = 10

def get_data(offset):

    url = f"https://sef.podkolzin.consulting/api/users/lastSeen?offset={offset}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data['data']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

def update_data(user, previous_state):
    user_id = user['userId']
    is_online = user['isOnline']
    if user_id in previous_state:
        previous_user = previous_state[user_id]
        user['onlinePeriods'] = previous_user['onlinePeriods'] if is_online else previous_user['onlinePeriods'][:-1] + [[previous_user['onlinePeriods'][-1][0], datetime.now().isoformat()]]
    else:
        user['onlinePeriods'] = [[datetime.now().isoformat(), None]] if is_online else []
    return user

def fand_update_data():
    offset = 0
    all_data = []
    while True:
        data = get_data(offset)
        if not data:
            break
        for d in data:
            user = {'userId': d['userId'], 'isOnline': d['isOnline'], 'lastSeenDate': d['lastSeenDate']}
            updated_user = update_user_data(user, previous_state)
            all_data.append(updated_user)
            previous_state[updated_user['userId']] = updated_user
        offset += len(data)
    with open(DATA_FILE, 'w') as f:
        json.dump(all_data, f)

def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def get_users_online(date):

    all_data = load_data()
    users_online = 0
    for user in all_data:
        for period in user['onlinePeriods']:
            start = datetime.fromisoformat(period[0])
            end = datetime.fromisoformat(period[1]) if period[1] else datetime.now()
            if start <= date <= end:
                users_online += 1
                break
    return users_online


if __name__ == "__main__":
    previous_state = load_data()
    while True:
        fand_update_data()
        time.sleep(FETCH_INTERVAL)
