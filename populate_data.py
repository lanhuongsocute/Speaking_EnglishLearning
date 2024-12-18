from app import app, db
from app.models import Topic, SpeakingQuestion

# Dữ liệu mẫu
data = {
    1: {"topic": "Personal Information", "questions": [
        "What is your name?",
        "Where are you from?",
        "Can you describe your family?"
    ]},
    2: {"topic": "Hobbies and Interests", "questions": [
        "What do you like to do in your free time?",
        "Do you have any hobbies?",
        "Why do you enjoy your hobbies?"
    ]},
    3: {"topic": "Daily Activities", "questions": [
        "Can you describe your typical day?",
        "What do you usually do in the morning?",
        "How do you spend your evenings?"
    ]},
    4: {"topic": "Future Plans", "questions": [
        "What are your plans for the future?",
        "Do you have any career goals?",
        "Where would you like to travel in the future?"
    ]},
    5: {"topic": "Travel and Holidays", "questions": [
        "Where did you go on your last holiday?",
        "What do you like about traveling?",
        "Can you describe your ideal vacation?"
    ]}
}

# Sử dụng ngữ cảnh ứng dụng
with app.app_context():
    # Thêm dữ liệu vào cơ sở dữ liệu
    for key, value in data.items():
        # Thêm Topic
        topic = Topic(name=value["topic"], description=f"Description for {value['topic']}")
        db.session.add(topic)
        db.session.commit()

        # Thêm Speaking Questions liên quan đến Topic
        for question in value["questions"]:
            speaking_question = SpeakingQuestion(content=question, topic_id=topic.id)
            db.session.add(speaking_question)

    # Commit tất cả thay đổi
    db.session.commit()
    print("Data populated successfully!")
