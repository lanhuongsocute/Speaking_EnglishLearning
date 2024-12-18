from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)  # Thêm cột is_admin
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    lessons = db.relationship('Lesson', backref='topic', lazy=True)  # Một chủ đề có nhiều bài học
    vocabularies = db.relationship('Vocabulary', backref='topic', lazy=True)  # Một chủ đề có nhiều từ vựng
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    challenges = db.relationship('Challenge', backref='topic', lazy=True)
    
class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    lesson_type = db.Column(db.String(50), default="normal")
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)  # Bài học thuộc một chủ đề
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Vocabulary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100), nullable=False)
    meaning = db.Column(db.String(250), nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)  # Từ vựng thuộc một chủ đề
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)  # Nội dung câu hỏi
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)  # Câu hỏi thuộc bài học nào
    question_type = db.Column(db.String(50), default="text")  # Loại câu hỏi: 'text' hoặc 'multiple-choice'
    choices = db.relationship('Choice', backref='question', lazy=True)  # Quan hệ 1-n với bảng Choice
    answer = db.Column(db.String(255), nullable=True)  # Đáp án (nếu là câu hỏi tự luận hoặc câu trả lời chính)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)  # Nội dung lựa chọn
    is_correct = db.Column(db.Boolean, default=False)  # Đánh dấu lựa chọn này có đúng hay không
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)  # Thuộc câu hỏi nào
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=True)  # Khóa ngoại đến bài học
    is_learned = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Challenge(db.Model):
    __tablename__ = 'challenge'  # Tên bảng trong cơ sở dữ liệu
    id = db.Column(db.Integer, primary_key=True)  # Sử dụng 'id' thay vì 'challenge_id'
    content = db.Column(db.Text, nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    hints = db.relationship('Hint', backref='challenge', lazy=True)  # Liên kết 1-n với bảng hint

class Hint(db.Model):
    __tablename__ = 'hint'  # Tên bảng trong cơ sở dữ liệu
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('challenge.id'), nullable=False)  # Liên kết với 'challenge.id'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)