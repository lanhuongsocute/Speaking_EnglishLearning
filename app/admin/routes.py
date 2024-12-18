from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import db, Topic, Lesson, Vocabulary, Question, Choice, User, Challenge, Hint
import os
from werkzeug.utils import secure_filename
from app.decorators import admin_required
from datetime import datetime

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

UPLOAD_FOLDER = 'app/static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Kiểm tra xem tệp có phải là hình ảnh hợp lệ không
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Kiểm tra quyền admin
def is_admin():
    return session.get('is_admin', False)  # Kiểm tra trong session có phải admin không

# ---------------------------------------------------Dashboard---------------------------------------------------
@admin_required
@admin.route('/')
def admin_dashboard():
    if not is_admin():
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('index'))  # Chuyển hướng đến trang chính nếu không phải admin
    
    lessons = Lesson.query.all()
    topics = Topic.query.all()
    return render_template('admin_dashboard.html', lessons=lessons, topics=topics)

# ---------------------------------------------------User---------------------------------------------------
@admin_required
@admin.route('/user_list')
def user_list():
    users = User.query.all()
    return render_template('admin_user_list.html', users=users)

@admin_required
@admin.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    
    # Kiểm tra nếu người dùng đang chỉnh sửa tài khoản admin@gmail.com
    if user.email == "admin@gmail.com":
        flash("Bạn không thể chỉnh sửa tài khoản admin", "danger")
        return redirect(url_for('admin.user_list'))  # Quay lại danh sách người dùng hoặc trang khác
    
    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        user.is_admin = 'is_admin' in request.form  # Cập nhật quyền admin (nếu cần)
        
        db.session.commit()
        flash('Thông tin người dùng đã được cập nhật!', 'success')
        return redirect(url_for('admin.user_list'))

    return render_template('admin_edit_user.html', user=user)

# Route để quản lý quyền của người dùng
@admin_required
@admin.route('/change_user_role/<int:user_id>', methods=['GET', 'POST'])
def change_user_role(user_id):
    user = User.query.get_or_404(user_id)

    # Nếu người dùng đang cố gắng thay đổi quyền của admin@gmail.com, ngừng hành động
    if user.email == 'admin@gmail.com':
        flash('Không thể thay đổi quyền của tài khoản admin@gmail.com', 'danger')
        return redirect(url_for('admin.user_list'))
    
    if request.method == 'POST':
        # Logic thay đổi quyền người dùng
        user.is_admin = 'is_admin' in request.form
        db.session.commit()
        flash(f'Quyền của người dùng {user.username} đã được thay đổi', 'success')
        return redirect(url_for('admin.user_list'))

    return render_template('admin_change_role.html', user=user)

@admin_required
@admin.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    # Kiểm tra nếu người dùng đang cố gắng xóa tài khoản admin@gmail.com
    if user.email == "admin@gmail.com":
        flash("Bạn không thể xóa tài khoản admin", "danger")
        return redirect(url_for('admin.user_list'))  # Quay lại danh sách người dùng hoặc trang khác

    # Xóa người dùng
    db.session.delete(user)
    db.session.commit()

    flash('Người dùng đã bị xóa thành công!', 'danger')
    return redirect(url_for('admin.user_list'))  # Quay lại danh sách người dùng


# ---------------------------------------------------Topic---------------------------------------------------
# Thêm Topic
@admin_required
@admin.route('/add-topic', methods=['GET', 'POST'])

def admin_add_topic():
    if not is_admin():
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        image = request.files.get('image')

        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            image.save(image_path)
            topic = Topic(name=name, description=description, image_url=filename)
        else:
            topic = Topic(name=name, description=description)

        db.session.add(topic)
        db.session.commit()

        flash('Topic added successfully!', 'success')
        return redirect(url_for('admin.admin_dashboard'))
    return render_template('admin_add_topic.html')

@admin_required
@admin.route('/admin-topic-list')
def admin_topic_list():
    if not is_admin():
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('index'))  # Chuyển hướng đến trang chính nếu không phải admin

    topics = Topic.query.all()
    return render_template('admin_topic_list.html',topics=topics)

@admin_required
@admin.route('/admin/edit_topic/<int:id>', methods=['GET', 'POST'])
def edit_topic(id):
    topic = Topic.query.get_or_404(id)  # Lấy chủ đề theo ID
    if request.method == 'POST':
        topic.name = request.form['name']
        topic.description = request.form['description']
        
        if 'image' in request.files:
            image = request.files.get('image')
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image_path = os.path.join(UPLOAD_FOLDER, filename)
                image.save(image_path)
                topic.image_url = image.filename
        
        db.session.commit()
        flash('Chủ đề đã được cập nhật thành công', 'success')
        return redirect(url_for('admin.admin_topic_list'))  # Quay lại danh sách chủ đề

    return render_template('admin_edit_topic.html', topic=topic)

@admin_required
@admin.route('/delete_topic/<int:id>', methods=['POST'])
def delete_topic(id):
    # Kiểm tra trường _method trong POST request để giả lập phương thức DELETE
    if request.form.get('_method') == 'DELETE':
        topic = Topic.query.get_or_404(id)
        
        # Xóa chủ đề
        db.session.delete(topic)
        db.session.commit()
        flash('Chủ đề đã bị xóa', 'danger')
        return redirect(url_for('admin.admin_topic_list'))

    # Nếu không phải phương thức DELETE, thông báo lỗi
    flash('Invalid request method', 'danger')
    return redirect(url_for('admin.admin_topic_list'))

# ---------------------------------------------------Lesson---------------------------------------------------
# Thêm Lesson
@admin_required
@admin.route('/add-lesson', methods=['GET', 'POST'])
def admin_add_lesson():
    if request.method == 'POST':
        title = request.form.get('title')  # Sử dụng get để tránh lỗi khi không có key
        content = request.form.get('content')
        topic_id = request.form.get('topic_id')
        lesson_type = request.form.get('lesson_type')  # Kiểu bài tập (normal/vocabulary)
        
        # Kiểm tra xem topic_id có hợp lệ không
        topic = Topic.query.get(topic_id)
        if not topic:
            flash('Topic not found!', 'error')
            return redirect(url_for('admin.admin_dashboard'))

        # Xử lý ảnh cho bài học và từ vựng (chung)
        file = request.files.get('file')
        file_path = None
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)

        # Thêm bài học bình thường
        lesson = Lesson(title=title, content=content, topic_id=topic_id, lesson_type=lesson_type, image_url=filename)
        db.session.add(lesson)
        db.session.commit()
        flash('Lesson added successfully!', 'success')

        return redirect(url_for('admin.admin_dashboard'))

    # Nếu không phải là phương thức POST, trả về trang thêm bài học
    topics = Topic.query.all()
    return render_template('admin_add_lesson.html', topics=topics)

# Sửa Lesson
@admin_required
@admin.route('/admin-lesson-list')
def admin_lesson_list():
    if not is_admin():
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('index'))  # Chuyển hướng đến trang chính nếu không phải admin

    lessons = Lesson.query.all()
    return render_template('admin_lesson_list.html',lessons=lessons)

@admin_required
@admin.route('/edit_lesson/<int:lesson_id>', methods=['GET', 'POST'])
def admin_edit_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    topics = Topic.query.all()
    
    if request.method == 'POST':
        try:
            # Gán dữ liệu từ form
            lesson.title = request.form['title']
            lesson.content = request.form['content']
            lesson.topic_id = int(request.form.get('topic_id'))
            lesson.lesson_type = request.form.get('lesson_type')
            
            # Xử lý hình ảnh
            if 'image' in request.files:
                image = request.files.get('image')
                if image and allowed_file(image.filename):
                    filename = secure_filename(image.filename)
                    image_path = os.path.join(UPLOAD_FOLDER, filename)
                    image.save(image_path)
                    lesson.image_url = image.filename
            
            db.session.commit()  # Lưu thay đổi
            flash('Bài học đã được cập nhật thành công!', 'success')
            return redirect(url_for('admin.admin_lesson_list'))
        except Exception as e:
            db.session.rollback()  # Rollback nếu xảy ra lỗi
            flash(f'Đã xảy ra lỗi: {e}', 'danger')
            print(f'Lỗi: {e}')  # Debug lỗi
    
    return render_template('admin_edit_lesson.html', lesson=lesson, topics=topics)

# Xóa Lesson
@admin_required
@admin.route('/delete-lesson/<int:lesson_id>', methods=['POST'])
def admin_delete_lesson(lesson_id):
    if not is_admin():
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('index'))

    lesson = Lesson.query.get_or_404(lesson_id)
    db.session.delete(lesson)
    db.session.commit()
    flash('Lesson deleted successfully!', 'success')
    return redirect(url_for('admin.admin_dashboard'))

# ---------------------------------------------------Vocabulary---------------------------------------------------
# Thêm vocabulary
@admin_required
@admin.route('/vocabulary_list')
def vocabulary_list():
    vocabularies = Vocabulary.query.all()
    return render_template('admin_vocabulary_list.html', vocabularies=vocabularies)

@admin_required
@admin.route('/add_vocabulary', methods=['GET', 'POST'])
def add_vocabulary():
    topics = Topic.query.all()  # Lấy tất cả các chủ đề để chọn cho từ vựng

    if request.method == 'POST':
        word = request.form['word']
        meaning = request.form['meaning']
        topic_id = request.form['topic_id']
        
        # Kiểm tra xem có file hình ảnh không
        image_url = None
        if 'image' in request.files:
            image = request.files['image']
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image_path = os.path.join(UPLOAD_FOLDER, filename)
                image.save(image_path)
                image_url = filename

        # Tạo đối tượng Vocabulary mới và lưu vào CSDL
        new_vocabulary = Vocabulary(word=word, meaning=meaning, image_url=image_url, topic_id=topic_id)
        db.session.add(new_vocabulary)
        db.session.commit()

        flash('Từ vựng đã được thêm thành công!', 'success')
        return redirect(url_for('admin.vocabulary_list'))  # Quay lại danh sách từ vựng

    return render_template('admin_add_vocabulary.html', topics=topics)

# Sửa vocabulary
@admin_required
@admin.route('/edit_vocabulary/<int:vocabulary_id>', methods=['GET', 'POST'])
def edit_vocabulary(vocabulary_id):
    vocabulary = Vocabulary.query.get_or_404(vocabulary_id)
    topics = Topic.query.all()  # Lấy tất cả các chủ đề

    if request.method == 'POST':
        vocabulary.word = request.form['word']
        vocabulary.meaning = request.form['meaning']
        vocabulary.topic_id = request.form['topic_id']

        # Nếu có ảnh mới, xử lý như bài học trước
        if 'image' in request.files:
            image = request.files.get('image')
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image_path = os.path.join(UPLOAD_FOLDER, filename)
                image.save(image_path)
                vocabulary.image_url = filename

        db.session.commit()
        flash('Từ vựng đã được cập nhật thành công!', 'success')
        return redirect(url_for('admin.vocabulary_list'))  # Quay lại danh sách từ vựng

    return render_template('admin_edit_vocabulary.html', vocabulary=vocabulary, topics=topics)

# Xóa vocabulary
@admin_required
@admin.route('/delete_vocabulary/<int:vocabulary_id>', methods=['POST'])
def delete_vocabulary(vocabulary_id):
    vocabulary = Vocabulary.query.get_or_404(vocabulary_id)
    db.session.delete(vocabulary)
    db.session.commit()
    flash('Từ vựng đã bị xóa thành công!', 'success')
    return redirect(url_for('admin.vocabulary_list'))  # Quay lại danh sách từ vựng

# ---------------------------------------------------Question---------------------------------------------------
@admin_required
@admin.route('/add-question', methods=['GET', 'POST'])
def add_question():
    from app.models import Question, Choice, Lesson

    lessons = Lesson.query.all()  # Lấy danh sách bài học để hiển thị
    if request.method == 'POST':
        content = request.form.get('content', '').strip()  # Loại bỏ khoảng trắng thừa
        lesson_id = request.form.get('lesson_id')
        question_type = request.form.get('question_type', 'text').strip()
        add_choice = request.form.get('add_choice', 'false').lower()  # Xử lý giá trị 'true' hoặc 'false'

        # Kiểm tra dữ liệu đầu vào
        if not content:
            flash('Nội dung câu hỏi không được để trống.', 'danger')
            return redirect(url_for('admin.add_question'))

        if not lesson_id or not lesson_id.isdigit():
            flash('Vui lòng chọn một bài học hợp lệ.', 'danger')
            return redirect(url_for('admin.add_question'))

        # Kiểm tra tồn tại của bài học
        lesson = Lesson.query.get(int(lesson_id))
        if not lesson:
            flash('Bài học không tồn tại.', 'danger')
            return redirect(url_for('admin.add_question'))

        # Thêm câu hỏi mới
        question = Question(content=content, lesson_id=lesson.id, question_type=question_type)
        db.session.add(question)
        db.session.commit()

        # Xử lý lựa chọn thêm câu trả lời
        if add_choice == 'true':
            flash('Câu hỏi đã được thêm. Hãy thêm các lựa chọn.', 'info')
            return redirect(url_for('admin.add_choice', question_id=question.id))

        # Hoàn tất nếu không thêm lựa chọn
        flash('Câu hỏi đã được thêm thành công.', 'success')
        return redirect(url_for('admin.add_question'))

    return render_template('admin_add_question.html', lessons=lessons)

@admin_required
@admin.route('/question-list')
def admin_question_list():
    from app.models import Question
    questions = Question.query.all()
    return render_template('admin_question_list.html', questions=questions)

@admin_required
@admin.route('/update-question/<int:question_id>', methods=['GET', 'POST'])
def update_question(question_id):
    from app.models import Question
    question = Question.query.get_or_404(question_id)

    if request.method == 'POST':
        # Cập nhật thông tin
        question.content = request.form['content']
        question.lesson_id = request.form['lesson_id']
        question.question_type = request.form['question_type']
        db.session.commit()
        flash('Câu hỏi đã được cập nhật!', 'success')
        return redirect(url_for('admin.admin_question_list'))
    
    lessons = Lesson.query.all()  # Lấy danh sách bài học
    return render_template('admin_edit_question.html', question=question, lessons=lessons)

@admin_required
@admin.route('/delete-question/<int:question_id>', methods=['POST'])
def delete_question(question_id):
    from app.models import Question, Choice
    question = Question.query.get_or_404(question_id)
    
    # Xóa tất cả các choice liên quan
    Choice.query.filter_by(question_id=question.id).delete()
    
    db.session.delete(question)
    db.session.commit()
    flash('Câu hỏi đã được xóa thành công!', 'success')
    return redirect(url_for('admin.admin_question_list'))



# ---------------------------------------------------Choice---------------------------------------------------
@admin_required
@admin.route('/add-choice/<int:question_id>', methods=['GET', 'POST'])
def add_choice(question_id):
    from app.models import Choice, Question

    question = Question.query.get_or_404(question_id)
    if request.method == 'POST':
        # Lấy các choice từ form
        choices = request.form.getlist('choices[]')
        correct_choice_index = int(request.form.get('correct_choice'))  # Lấy index của đáp án đúng

        # Thêm choices vào cơ sở dữ liệu
        for idx, choice_content in enumerate(choices):
            is_correct = (idx == correct_choice_index)  # Đáp án đúng
            choice = Choice(content=choice_content, is_correct=is_correct, question_id=question.id)
            db.session.add(choice)

            # Nếu là đáp án đúng, lưu nội dung vào cột answer của question
            if is_correct:
                question.answer = choice_content

        db.session.commit()
        flash('Choice đã được thêm thành công và đáp án đúng đã được lưu.', 'success')
        return redirect(url_for('admin.add_question'))

    return render_template('admin_add_choice.html', question=question)

@admin_required
@admin.route('/manage-choices/<int:question_id>', methods=['GET', 'POST'])
def manage_choices(question_id):
    from app.models import Question, Choice
    question = Question.query.get_or_404(question_id)
    choices = Choice.query.filter_by(question_id=question_id).all()

    if request.method == 'POST':
        # Lấy danh sách các lựa chọn từ form
        choices_data = request.form.getlist('choices[]')
        correct_choice_index = int(request.form.get('correct_choice'))

        # Xóa các choice cũ
        Choice.query.filter_by(question_id=question_id).delete()

        # Thêm các choice mới
        for idx, choice_content in enumerate(choices_data):
            is_correct = (idx == correct_choice_index)
            choice = Choice(content=choice_content, is_correct=is_correct, question_id=question.id)
            db.session.add(choice)
            
            # Nếu là đáp án đúng, cập nhật vào cột answer
            if is_correct:
                question.answer = choice_content

        db.session.commit()
        flash('Choices đã được cập nhật!', 'success')
        return redirect(url_for('admin.admin_question_list'))
    
    return render_template('manage_choices.html', question=question, choices=choices)

@admin_required
@admin.route('/edit_choice/<int:choice_id>', methods=['GET', 'POST'])
def edit_choice(choice_id):
    choice = Choice.query.get_or_404(choice_id)

    if request.method == 'POST':
        choice.content = request.form['content']
        choice.is_correct = 'is_correct' in request.form

        db.session.commit()
        flash('Lựa chọn đã được cập nhật!', 'success')
        return redirect(url_for('admin.question_details', question_id=choice.question_id))

    return render_template('admin_edit_choice.html', choice=choice)

@admin_required
@admin.route('/delete_choice/<int:choice_id>', methods=['POST'])
def delete_choice(choice_id):
    choice = Choice.query.get_or_404(choice_id)
    db.session.delete(choice)
    db.session.commit()

    flash('Lựa chọn đã được xóa!', 'success')
    return redirect(url_for('admin.question_details', question_id=choice.question_id))

# -----------------------------------------Challenge---------------------------------------------------------
@admin_required
@admin.route('/add-challenge', methods=['GET', 'POST'])
def add_challenge():
    topics = Topic.query.all()  # Lấy danh sách topic từ database
    if request.method == 'POST':
        # Lấy dữ liệu từ form
        topic_id = request.form['topic']
        question_content = request.form['question']
        hints = [request.form.get(f'hint{i}') for i in range(1, 4)]

        # Tạo câu hỏi speaking_challenge
        challenge = Challenge(content=question_content, topic_id=topic_id)
        db.session.add(challenge)
        db.session.commit()

        # Thêm các gợi ý
        for hint_content in hints:
            if hint_content:  # Kiểm tra nếu có nội dung gợi ý
                hint = Hint(content=hint_content, question_id=challenge.id)
                db.session.add(hint)

        db.session.commit()
        flash('Challenge and hints added successfully!', 'success')
        return redirect(url_for('admin.admin_dashboard'))

    return render_template('admin_add_challenge.html', topics=topics)

@admin_required
@admin.route('/challenge-list', methods=['GET'])
def admin_challenge_list():
    challenges = Challenge.query.all()  # Lấy tất cả câu hỏi
    return render_template('admin_challenge_list.html', challenges=challenges)

@admin_required
@admin.route('/edit-challenge/<int:challenge_id>', methods=['GET', 'POST'])
def edit_challenge(challenge_id):
    challenge = Challenge.query.get_or_404(challenge_id)
    hints = Hint.query.filter_by(question_id=challenge.id).all()
    topics = Topic.query.all()  

    if request.method == 'POST':
        challenge.content = request.form['question']
        challenge.topic_id = request.form['topic']

        for idx, hint in enumerate(hints):
            hint_content = request.form.get(f'hint{idx+1}')
            if hint_content:
                hint.content = hint_content

        db.session.commit()
        flash('Challenge updated successfully!', 'success')
        return redirect(url_for('admin.admin_challenge_list'))

    return render_template('admin_edit_challenge.html', challenge=challenge, hints=list(enumerate(hints, start=1)), topics=topics)

@admin_required
@admin.route('/delete-challenge/<int:challenge_id>', methods=['POST'])
def delete_challenge(challenge_id):
    challenge = Challenge.query.get_or_404(challenge_id)
    hints = Hint.query.filter_by(question_id=challenge.id).all()

    for hint in hints:
        db.session.delete(hint)

    db.session.delete(challenge)
    db.session.commit()
    flash('Challenge deleted successfully!', 'success')
    return redirect(url_for('admin.admin_challenge_list'))
