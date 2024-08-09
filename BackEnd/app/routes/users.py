from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import db, User

users_bp = Blueprint('users', __name__)

@users_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    current_user = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({'message': 'User not found'}), 404

    if current_user['id'] != user_id and not current_user['is_admin']:
        return jsonify({'message': 'Access forbidden'}), 403

    return jsonify(user.to_dict()), 200

@users_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    current_user = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({'message': 'User not found'}), 404

    if current_user['id'] != user_id and not current_user['is_admin']:
        return jsonify({'message': 'Access forbidden'}), 403

    data = request.get_json()
    user.email = data.get('email', user.email)
    user.name = data.get('name', user.name)
    user.phone = data.get('phone', user.phone)
    user.address = data.get('address', user.address)
    user.ethnicity = data.get('ethnicity', user.ethnicity)
    user.religion = data.get('religion', user.religion)
    user.gender = data.get('gender', user.gender)
    user.cccd = data.get('cccd', user.cccd)

    db.session.commit()
    return jsonify({'message': 'User updated successfully'}), 200
