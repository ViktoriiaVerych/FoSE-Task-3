from marshmallow import Schema, fields, validate
from flask_sqlalchemy import SQLAlchemy
from models import User, Prediction
from flask_restful import reqparse, abort
import config
from flask import Flask, request, jsonify
from datetime import datetime
import data_procession as dp

app = Flask(__name__)
db = SQLAlchemy(app)

class UserStatsSchema(Schema):
    date = fields.Date(required=True)
    userId = fields.Str(required=True)
    tolerance = fields.Float(required=True)

arg_parser = UserStatsSchema()

@app.route('/api/stats/user', methods=['GET'])
def get_user_stats():
    args = arg_parser.parse_args()
    date_str = args['date']
    user_id = args['userId']
    date = datetime.fromisoformat(date_str)
    user_data = User.query.filter_by(date=date, user_id=user_id).first()
    
    if user_data is None:
        abort(404, 'Invalid userId')
    return jsonify(user_data)

@app.route('/api/predictions/users', methods=['GET'])
def get_users_predictions():
    args = arg_parser.parse_args()
    date_str = args['date']
    date = datetime.fromisoformat(date_str)
    prediction = Prediction.query.filter_by(date=date).all()
    
    return jsonify(prediction)

@app.route('/api/predictions/user', methods=['GET'])
def get_user_prediction():
    args = arg_parser.parse_args()
    date_str = args['date']
    user_id = args['userId']
    tolerance = args['tolerance']
    date = datetime.fromisoformat(date_str)
    prediction = Prediction.query.filter_by(date=date, user_id=user_id).first()
    
    if prediction is None:
        abort(404)
    prediction['willBeOnline'] = prediction['onlineChance'] >= tolerance
    return jsonify(prediction)

@app.route('/api/stats/users', methods=['GET'])
def get_users_stats():
    args = arg_parser.parse_args()
    date_str = args['date']
    date = datetime.fromisoformat(date_str)
    users_online = User.query.filter_by(date=date).count()
    
    return jsonify({'date': date_str, 'usersOnline': users_online})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
