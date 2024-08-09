from flask import Blueprint, request, jsonify, render_template, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import db, Cart, Book, User, Bill, BillInfo
from datetime import datetime

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/', methods=['GET'])
@jwt_required()
def get_cart():
    current_user = get_jwt_identity()
    user = User.query.get(current_user['id'])
    if not user:
        return jsonify({'message': 'User not found'}), 404

    cart_items = Cart.query.filter_by(user_id=user.id, status='unpaid').all()
    return jsonify([{
        'book_id': item.book_id,
        'title': item.book.title,
        'author': item.book.author,
        'price': "{:,.0f} VND".format(item.book.price).replace(",", "."),
        'quantity': item.quantity
    } for item in cart_items]), 200

@cart_bp.route('/', methods=['POST'])
@jwt_required()
def add_to_cart():
    current_user = get_jwt_identity()
    user = User.query.get(current_user['id'])
    if not user:
        return jsonify({'message': 'User not found'}), 404

    data = request.get_json()
    book_id = data.get('book_id')
    quantity = data.get('quantity', 1)

    if not book_id:
        return jsonify({'message': 'Book ID is required'}), 400

    book = Book.query.get(book_id)
    if not book:
        return jsonify({'message': 'Book not found'}), 404

    cart_item = Cart.query.filter_by(user_id=user.id, book_id=book_id, status='unpaid').first()

    if cart_item:
        cart_item.quantity += quantity
    else:
        new_cart_item = Cart(user_id=user.id, book_id=book_id, quantity=quantity, status='unpaid')
        db.session.add(new_cart_item)

    db.session.commit()
    return jsonify({'message': 'Book added to cart'}), 201

@cart_bp.route('/checkout', methods=['POST'])
@jwt_required()
def checkout():
    current_user = get_jwt_identity()
    user = User.query.get(current_user['id'])
    if not user:
        return jsonify({'message': 'User not found'}), 404

    cart_items = Cart.query.filter_by(user_id=user.id, status='unpaid').all()

    if not cart_items:
        return jsonify({'message': 'Cart is empty'}), 400

    total_price = sum(item.book.price * item.quantity for item in cart_items)

    for item in cart_items:
        item.status = 'paid'
        item.purchase_date = datetime.utcnow()  

    db.session.commit()

    # Tạo thông tin bill
    items = [{
        'title': item.book.title,
        'author': item.book.author,
        'quantity': item.quantity,
        'price': "{:,.0f} VND".format(item.book.price).replace(",", "."),
        'total_price': "{:,.0f} VND".format(item.book.price * item.quantity).replace(",", ".")
    } for item in cart_items]

    html = render_template('bill.html', user_name=user.name, user_email=user.email, purchase_date=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"), items=items, total_price="{:,.0f} VND".format(total_price).replace(",", "."))

    response = make_response(html)
    response.headers['Content-Type'] = 'text/html'
    response.headers['Content-Disposition'] = 'attachment; filename=bill.html'
    return response
