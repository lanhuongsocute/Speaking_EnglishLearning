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

# Import các models
from app.models import *

# Import các routes
from app.routes import *

if __name__ == "__main__":
    app.run(debug=True)
