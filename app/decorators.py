from functools import wraps
from flask import redirect, url_for, session, flash

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session or not session['user'].get('is_admin', False):
            return redirect(url_for('login'))  # Nếu không phải admin, chuyển hướng đến trang đăng nhập
        return f(*args, **kwargs)
    return decorated_function

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):  # Kiểm tra nếu chưa đăng nhập
            flash("You need to login first!", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


