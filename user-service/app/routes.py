from flask import Blueprint, request, jsonify, current_app, redirect, url_for
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_access_token
from app.models import User
from app import db

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'User already exists'}), 400

    hashed_password = generate_password_hash(data['password'])
    new_user = User(username=data['username'], password=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    user_id = new_user.id
    access_token = create_access_token(identity={'id': user_id, 'username': new_user.username})
    current_app.logger.info(f"Generated JWT: {access_token}") 

    return jsonify({
        'message': 'User registered successfully',
        'user': {
            'id': user_id,
            'username': new_user.username
        },
        'access_token': access_token
    }), 201

@bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()

        if not data or 'username' not in data or 'password' not in data:
            current_app.logger.warning("Missing username or password in request")
            return jsonify({'message': 'Missing credentials'}), 400
        
        user = User.query.filter_by(username=data['username']).first()

        if user and check_password_hash(user.password, data['password']):
            access_token = create_access_token(identity={'id': user.id, 'username': user.username})
            current_app.logger.info(f"Generated JWT: {access_token}") 
            return jsonify({'access_token': access_token}), 200
        else:
            return jsonify({'message': 'Invalid credentials'}), 401
    
    elif request.method == 'GET':
        return redirect('http://localhost/index.html')

@bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    return jsonify({'logged_in_as': current_user}), 200

@bp.route('/api/verify', methods=['GET'])
@jwt_required()
def verify():
    current_user = get_jwt_identity()
    print(f"Current User: {current_user}")
    return jsonify({'user': current_user}), 200
