from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import db, Book, User, Cart
import random
books_bp = Blueprint('books', __name__)

@books_bp.route('/', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([book.to_dict() for book in books]), 200

@books_bp.route('/<int:id>', methods=['GET'])
def get_book(id):
    book = Book.query.get_or_404(id)
    return jsonify(book.to_dict()), 200


@books_bp.route('/search', methods=['GET'])
def search_books():
    query = request.args.get('query')
    if not query:
        return jsonify({'message': 'Query parameter is required'}), 400

    books = Book.query.filter(
        (Book.title.ilike(f'%{query}%')) |
        (Book.author.ilike(f'%{query}%')) |
        (Book.category.ilike(f'%{query}%'))
    ).all()

    return jsonify([{
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'category': book.category,
        'year': book.year,
        'price': f"{book.price:.3f} VND",
        'stock': book.stock,
        'image_url': book.image_url
    } for book in books]), 200

@books_bp.route('/random', methods=['GET'])
def get_random_books():
    num_books = request.args.get('num_books', default=1, type=int)
    books = Book.query.all()
    if not books:
        return jsonify({'message': 'No books available'}), 404

    random_books = random.sample(books, min(num_books, len(books)))
    return jsonify([{
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'category': book.category,
        'year': book.year,
        'price': f"{book.price:.3f} VND",
        'stock': book.stock,
        'image_url': book.image_url
    } for book in random_books]), 200




@books_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_book(id):
    current_user = get_jwt_identity()
    user = User.query.get(current_user['id'])
    if not user or not user.is_admin:
        return jsonify({'message': 'Access forbidden'}), 403

    book = Book.query.get_or_404(id)

    # Xóa các mục trong giỏ hàng liên kết với quyển sách này
    Cart.query.filter_by(book_id=book.id).delete()

    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted'}), 200
