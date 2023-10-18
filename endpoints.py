from apscheduler.schedulers.background import BackgroundScheduler
from flask import Blueprint
from flask import Flask, request, jsonify
import data_procession
from datetime import datetime

app = Flask(__name__)

scheduler = BackgroundScheduler()
scheduler.add_job(data_procession.fetch_and_update_data, 'interval', minutes=60)
scheduler.start()

@app.route('/api/stats/user/online_time/<int:userId>', methods=['GET'])
def get_online_time(userId):
    user_data = data_procession.update_user_data(userId)
    
    if user_data is None:
        return jsonify({'error': 'Invalid userId'}), 404

    online_time = data_procession.calculate_online_time(user_data)
    return jsonify({'userId': userId, 'onlineTime': online_time})

@app.route('/api/stats/user/average/<int:userId>', methods=['GET'])
def get_average_times(userId):
    user_data = data_procession.update_user_data(userId)
    
    if user_data is None:
        return jsonify({'error': 'Invalid userId'}), 404

    weekly_avg, daily_avg = data_procession.calculate_average_times(user_data)
    return jsonify({'userId': userId, 'weeklyAverage': weekly_avg, 'dailyAverage': daily_avg})

@app.route('/api/user/forget', methods=['POST'])
def forget_user():
    request_body = request.get_json()
    userId = request_body.get('userId')
    
    if data_procession.check_user_exists(userId):
        data_procession.delete_user_data(userId)
        return jsonify({'userId': userId})
    else:
        return jsonify({'error': 'User does not exist'}), 404

@app.errorhandler(404)
def handle_invalid_user(error):
    return jsonify({'error': 'Invalid userId'}), 404

@app.errorhandler(500)
def handle_server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

stats_routes = Blueprint('stats_routes', __name__)

@stats_routes.route('/api/stats/user/online_time/<int:userId>', methods=['GET'])
def get_online_time(userId):
    user_data = data_procession.update_user_data(userId)

    if user_data is None:
        return handle_invalid_user(404)

    online_time = data_procession.calculate_online_time(user_data)
    return jsonify({'userId': userId, 'onlineTime': online_time})

@stats_routes.route('/api/stats/user/average/<int:userId>', methods=['GET'])
def get_average_times(userId):
    user_data = data_procession.update_user_data(userId)

    if user_data is None:
        return handle_invalid_user(404)

    weekly_avg, daily_avg = data_procession.calculate_average_times(user_data)
    return jsonify({'userId': userId, 'weeklyAverage': weekly_avg, 'dailyAverage': daily_avg})

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/api/user/forget', methods=['POST'])
def forget_user():
    request_body = request.get_json()
    userId = request_body.get('userId')

    if data_procession.check_user_exists(userId):
        data_procession.delete_user_data(userId)
        return jsonify({'userId': userId})
    else:
        return jsonify({'error': 'User does not exist'}), 404

app.register_blueprint(stats_routes)
app.register_blueprint(user_routes)

if __name__ == "__main__":
    app.run()