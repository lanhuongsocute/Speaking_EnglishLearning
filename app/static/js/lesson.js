// const lessonId = '{{ lesson.id }}';

function submitAnswers() {
    const form = document.getElementById('quiz-form');
    const formData = new FormData(form);
    const answers = {};

    // Thu thập câu trả lời của người dùng
    formData.forEach((value, key) => {
        const questionId = key.split('-')[1];
        answers[questionId] = value;
    });

    // Gửi dữ liệu lên server
    fetch(`/lesson/${lessonId}/submit`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ answers: answers })
    })
    .then(response => response.json())
    .then(data => {
        if (data.is_completed) {
            alert('🎉 Lesson completed successfully!');
            document.getElementById('completion-status').innerHTML = 
                '<p class="text-success"><strong>🎉 Lesson Completed!</strong></p>';
            highlightAnswers(data.correct_answers, answers);
        } else {
            alert('Some answers are incorrect. Please try again.');
            highlightAnswers(data.correct_answers, answers);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while submitting answers.');
    });
}

// Hiển thị hiệu ứng xanh/đỏ
function highlightAnswers(correctAnswers, userAnswers) {
    const questions = document.querySelectorAll('.question-item');

    questions.forEach((question) => {
        const questionId = question.querySelector('input').name.split('-')[1];
        const correctAnswerId = correctAnswers[questionId];
        const userAnswerId = userAnswers[questionId];

        const choices = question.querySelectorAll('input[type="radio"]');
        choices.forEach(input => {
            const choiceElement = input.closest('li');
            choiceElement.style.backgroundColor = ""; // Xóa màu cũ

            if (input.value == correctAnswerId) {
                // Đáp án đúng
                choiceElement.style.backgroundColor = "#e0f8e0";
                choiceElement.style.color = "green";
            }
            if (input.checked && input.value != correctAnswerId) {
                // Đáp án sai
                choiceElement.style.backgroundColor = "#ffcccb";
                choiceElement.style.color = "red";
            }
        });
    });
}
    // Hiển thị hiệu ứng xanh/đỏ
    function highlightAnswers(correctAnswers, userAnswers) {
        const questions = document.querySelectorAll('.question-item');

        questions.forEach((question) => {
            const questionId = question.querySelector('input').name.split('-')[1];
            const correctAnswerId = correctAnswers[questionId];
            const userAnswerId = userAnswers[questionId];

            const choices = question.querySelectorAll('input[type="radio"]');
            choices.forEach(input => {
                const choiceElement = input.closest('li');

                // Xóa hiệu ứng cũ
                choiceElement.style.backgroundColor = "";
                choiceElement.style.color = "";

                // Đánh dấu đáp án đúng
                if (input.value == correctAnswerId) {
                    choiceElement.style.backgroundColor = "#e0f8e0";  // Xanh nhạt
                    choiceElement.style.color = "green";
                }

                // Đánh dấu đáp án người dùng chọn sai
                if (input.checked && input.value != correctAnswerId) {
                    choiceElement.style.backgroundColor = "#ffcccb";  // Đỏ nhạt
                    choiceElement.style.color = "red";
                }
            });
        });
    }


    