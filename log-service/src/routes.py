from flask import Blueprint, jsonify
from src import mongo

log_bp = Blueprint('log', __name__)

@log_bp.route('/')
def index():
    return 'Log Service is running'

@log_bp.route('/logs', methods=['GET'])
def get_logs():
    logs = mongo.db.logs.find()
    log_list = [{"message": log['message'], "timestamp": log.get('timestamp')} for log in logs]
    return jsonify(log_list), 200
