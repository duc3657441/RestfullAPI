from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from ..models import db, User
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    phone = data.get('phone')
    address = data.get('address')
    ethnicity = data.get('ethnicity')
    religion = data.get('religion')
    gender = data.get('gender')
    cccd = data.get('cccd')
    is_admin = data.get('is_admin', False)

    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already registered'}), 400

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    new_user = User(
        email=email, password=hashed_password, name=name, phone=phone, address=address,
        ethnicity=ethnicity, religion=religion, gender=gender, cccd=cccd, is_admin=is_admin
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid email or password'}), 401

    access_token = create_access_token(identity={'id': user.id, 'email': user.email, 'is_admin': user.is_admin})
    return jsonify({'access_token': access_token}), 200
