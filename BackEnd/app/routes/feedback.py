from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import db, Feedback, User
from datetime import datetime

feedback_bp = Blueprint('feedback', __name__)

@feedback_bp.route('/', methods=['POST'])
@jwt_required()
def add_feedback():
    current_user = get_jwt_identity()
    data = request.get_json()
    
    feedback = Feedback(
        user_id=current_user['id'],
        book_id=data['book_id'],
        rating=data['rating'],
        comment=data['comment'],
        feedback_date=datetime.utcnow()  # Thêm giá trị cho feedback_date
    )

    db.session.add(feedback)
    db.session.commit()
    return jsonify({'message': 'Feedback added successfully'}), 201

@feedback_bp.route('/admin', methods=['GET'])
@jwt_required()
def get_feedback():
    current_user = get_jwt_identity()
    user = User.query.get(current_user['id'])
    if not user or not user.is_admin:
        return jsonify({'message': 'Access forbidden'}), 403

    feedbacks = Feedback.query.all()
    return jsonify([{
        'user_id': feedback.user_id,
        'book_id': feedback.book_id,
        'rating': feedback.rating,
        'comment': feedback.comment,
        'feedback_date': feedback.feedback_date.strftime("%Y-%m-%d %H:%M:%S")
    } for feedback in feedbacks]), 200

@feedback_bp.route('/book/<int:book_id>', methods=['GET'])
@jwt_required()
def get_feedback_by_book(book_id):
    feedbacks = Feedback.query.filter_by(book_id=book_id).all()
    return jsonify([{
        'user_id': feedback.user_id,
        'book_id': feedback.book_id,
        'rating': feedback.rating,
        'comment': feedback.comment,
        'feedback_date': feedback.feedback_date.strftime("%Y-%m-%d %H:%M:%S")
    } for feedback in feedbacks]), 200
