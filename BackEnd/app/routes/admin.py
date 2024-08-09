from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import db, User, Feedback

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/feedback', methods=['GET'])
@jwt_required()
def get_feedback():
    current_user = get_jwt_identity()
    if not current_user['is_admin']:
        return jsonify({'message': 'Access forbidden'}), 403
    
    feedbacks = Feedback.query.all()
    return jsonify([feedback.to_dict() for feedback in feedbacks]), 200
