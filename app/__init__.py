from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

# Khởi tạo Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Khởi tạo SQLAlchemy và Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import routes và models
from app import routes, models

# Import và đăng ký Blueprint
from app.admin.routes import admin
app.register_blueprint(admin, url_prefix='/admin')

# Import các thành phần khác
from app import routes, models
