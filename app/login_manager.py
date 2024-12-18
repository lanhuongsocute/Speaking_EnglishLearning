from flask_login import LoginManager
from app import app
from app.models import User

login_manager = LoginManager()

def init_login_manager():
    login_manager.init_app(app)
    login_manager.login_view = 'login'  # Đường dẫn đến trang đăng nhập


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
