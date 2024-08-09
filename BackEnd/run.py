import os
from dotenv import load_dotenv
from app import create_app, db
from flask_migrate import Migrate

# Tải các biến môi trường từ tệp .env
load_dotenv()

app = create_app('development')
migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run()
