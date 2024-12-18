from app import app, db
from app.models import SpeakingQuestion, SpeakingAnswer

# Dữ liệu mẫu đáp án cho từng câu hỏi
answers_data = {
    "What is your name?": ["My name is John.", "I am Alice."],
    "Where are you from?": ["I am from New York.", "I am from Hanoi."],
    "Can you describe your family?": ["I have a small family with two siblings.", "I live with my parents and a younger sister."],
    "What do you like to do in your free time?": ["I like reading books.", "I enjoy watching movies."],
    "Do you have any hobbies?": ["Yes, I enjoy painting and hiking.", "I love playing guitar."],
    "Why do you enjoy your hobbies?": ["They help me relax.", "They make me feel creative."],
    "Can you describe your typical day?": ["I wake up early, go to work, and relax in the evening.", "I spend my day studying and exercising."],
    "What do you usually do in the morning?": ["I usually have breakfast and read the news.", "I go for a morning run."],
    "How do you spend your evenings?": ["I watch TV or spend time with my family.", "I read books or prepare for the next day."],
    "What are your plans for the future?": ["I plan to become a software developer.", "I want to travel the world."],
    "Do you have any career goals?": ["Yes, I want to be a team leader in my company.", "I aim to start my own business."],
    "Where would you like to travel in the future?": ["I would love to visit Japan.", "I want to explore Europe."],
    "Where did you go on your last holiday?": ["I went to the beach.", "I visited my grandparents in the countryside."],
    "What do you like about traveling?": ["I enjoy experiencing new cultures.", "I love meeting new people and trying new food."],
    "Can you describe your ideal vacation?": ["My ideal vacation is relaxing on a tropical island.", "I would love an adventurous trip to the mountains."]
}

# Sử dụng ngữ cảnh ứng dụng để truy cập cơ sở dữ liệu
with app.app_context():
    # Lấy tất cả các câu hỏi từ bảng speaking_questions
    questions = SpeakingQuestion.query.all()

    # Thêm mẫu đáp án cho từng câu hỏi
    for question in questions:
        if question.content in answers_data:
            for answer in answers_data[question.content]:
                new_answer = SpeakingAnswer(question_id=question.id, answer=answer)
                db.session.add(new_answer)

    # Lưu thay đổi
    db.session.commit()
    print("Sample answers added successfully!")
