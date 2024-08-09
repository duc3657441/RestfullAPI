import os
from dotenv import load_dotenv
from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

# Tải các biến môi trường từ tệp .env
load_dotenv()

app = create_app('development')
app.app_context().push()

def create_admin():
    admin_email = 'admin@example.com'
    admin_password = 'adminpassword'
    hashed_password = generate_password_hash(admin_password, method='pbkdf2:sha256')

    if not User.query.filter_by(email=admin_email).first():
        new_admin = User(email=admin_email, password=hashed_password, name='Admin User', is_admin=True)
        db.session.add(new_admin)
        db.session.commit()
        print("Admin user created")
    else:
        print("Admin user already exists")

if __name__ == "__main__":
    create_admin()
