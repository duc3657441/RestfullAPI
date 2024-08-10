from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import db, User, Feedback, Book
import os
from werkzeug.utils import secure_filename
from config import config
import random
import string
import datetime
admin_bp = Blueprint('admin', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    if not "." in filename:
        return False
    
    ext = filename.rsplit(".",1)[1]

    if ext.lower() in ALLOWED_EXTENSIONS :
        return True
    
    else:
        return False

def random_name():
    # Lấy thời gian hiện tại
    current_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    
    # Tạo chuỗi ký tự ngẫu nhiên
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    
    # Kết hợp thời gian và chuỗi ngẫu nhiên để tạo tên file
    file_name = f"{current_time}_{random_str}"
    
    return file_name



@admin_bp.route('/feedback', methods=['GET'])
@jwt_required()
def get_feedback():
    current_user = get_jwt_identity()
    if not current_user['is_admin']:
        return jsonify({'message': 'Access forbidden'}), 403
    
    feedbacks = Feedback.query.all()
    return jsonify([feedback.to_dict() for feedback in feedbacks]), 200

# chuc nang them sach trong admin
@admin_bp.route('/books', methods = ['POST'])
#@jwt_required()
def add_book():
    #current_user = get_jwt_identity()
    # if not current_user['is_admin']:
    #     return jsonify({'message': 'Access forbidden'}), 403
    title = request.form.get('title')
    
    author = request.form.get('author')
    category = request.form.get('category')
    year = request.form.get('year')
    price = request.form.get('price')
    stock = request.form.get('stock')
    
    # Lấy tệp hình ảnh
    image_file = request.files.get('image')
    
    required_fields = ['title', 'author', 'category', 'year', 'price', 'stock']
    for field in required_fields:
        if not request.form.get(field):
            return jsonify({'message': f'Missing required field: {field}'}), 400

    # Kiểm tra xem sách đã tồn tại chưa
    existing_book = Book.query.filter_by(title=title, author=author).first()
    if existing_book:
        return jsonify({'message': 'Book already exists'}), 409
    
    if not image_file:
        return jsonify({'message': 'Missing required field: image'}), 400
    if not allowed_file(image_file.filename):
        return jsonify({'message': 'This file is not an image '}), 400
    ext = image_file.filename.rsplit(".",1)[1]
    randomName = random_name() + "." + ext
    image_file.save(os.path.join("D:\\RestfullAPI\\FontEnd\\database",randomName))
    
    # Tạo đối tượng sách mới
    new_book = Book(
        title=title,
        author=author,
        category=category,
        year=int(year),
        price=float(price.replace(".", "").replace(",", "")),
        stock=int(stock),
        image_url= randomName
    )
    db.session.add(new_book)
    db.session.commit()
    return jsonify(new_book.to_dict()), 201
    data = request.get_json()
    
    required_fields = ['title', 'author', 'category', 'year', 'price', 'stock', 'image_url']

    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'Missing required field: {field}'}), 400
    
    existing_book = Book.query.filter_by(title=data['title'], author=data['author']).first()
    if existing_book:
        return jsonify({'message': 'Book already exists'}), 409

    new_book = Book(
        title=data['title'],
        author=data['author'],
        category=data['category'],
        year=int(data['year']),
        price=float(data['price'].replace(".", "").replace(",", "")),
        stock=int(data['stock']),
        image_url=data['image_url']
    )

    db.session.add(new_book)
    db.session.commit()
    return jsonify(new_book.to_dict()), 201