from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import db, Cart, User

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/', methods=['GET'])
@jwt_required()
def get_orders():
    current_user = get_jwt_identity()
    user = User.query.get(current_user['id'])
    if not user:
        return jsonify({'message': 'User not found'}), 404

    order_items = Cart.query.filter_by(user_id=user.id, status='paid').all()
    return jsonify([{
        'book_id': item.book_id,
        'title': item.book.title,
        'author': item.book.author,
        'price': "{:,.0f} VND".format(item.book.price).replace(",", "."),
        'quantity': item.quantity,
        'total_price': "{:,.0f} VND".format(item.book.price * item.quantity).replace(",", "."),
        'purchase_date': item.purchase_date.strftime("%Y-%m-%d %H:%M:%S") if item.purchase_date else None
    } for item in order_items]), 200
