from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(255))
    ethnicity = db.Column(db.String(50))  # Dân tộc
    religion = db.Column(db.String(50))   # Tôn giáo
    gender = db.Column(db.String(10))     # Giới tính
    cccd = db.Column(db.String(20))       # CCCD
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    carts = db.relationship('Cart', backref='user', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'phone': self.phone,
            'address': self.address,
            'ethnicity': self.ethnicity,
            'religion': self.religion,
            'gender': self.gender,
            'cccd': self.cccd,
            'is_admin': self.is_admin,
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
    
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(255))
    year = db.Column(db.Integer)
    price = db.Column(db.Float, nullable=False)
    #stock = db.Column(db.Integer, default=0)
    stock = db.Column(db.String(255), default='')

    image_url = db.Column(db.String(255))
    carts = db.relationship('Cart', backref='book', lazy=True)


    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'category': self.category,
            'year': self.year,
            'price': "{:,.0f} VND".format(self.price).replace(",", "."),
            'stock': self.stock,
            'image_url': self.image_url
        }

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), default='unpaid')
    purchase_date = db.Column(db.DateTime, nullable=True, default=None)

class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    purchase_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), default='unpaid')
    user = db.relationship('User', backref=db.backref('bills', lazy=True))

class BillInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bill_id = db.Column(db.Integer, db.ForeignKey('bill.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    purchase_date = db.Column(db.DateTime, nullable=False)
    bill = db.relationship('Bill', backref=db.backref('bill_infos', lazy=True))
    book = db.relationship('Book', backref=db.backref('bill_infos', lazy=True))
    
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(255))
    feedback_date = db.Column(db.DateTime, default=datetime.utcnow)  # Thêm mặc định

    user = db.relationship('User', backref=db.backref('feedbacks', lazy=True))
    book = db.relationship('Book', backref=db.backref('feedbacks', lazy=True))
