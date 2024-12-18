let recognition = null;
let isRecording = false;
let currentIndex = -1;

function startRecording(id) {
    if (isRecording && id !== currentIndex) {
        stopRecording(currentIndex); // Dừng ghi âm trước đó nếu đang chạy
    }

    recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'en-US';
    recognition.interimResults = true;

    recognition.onresult = (event) => {
        let finalTranscript = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
            const transcript = event.results[i][0].transcript;
            if (event.results[i].isFinal) {
                finalTranscript += transcript;
            }
        }
        document.getElementById(`result-${id}`).textContent = finalTranscript;
    };

    recognition.onend = () => {
        if (isRecording) recognition.start();
    };

    recognition.onerror = (event) => {
        alert("Error: " + event.error);
    };

    recognition.start();
    document.getElementById('status').textContent = "Status: Recording...";
    toggleButtons(id, true);

    isRecording = true;
    currentIndex = id;
}

function stopRecording(id) {
    if (!isRecording) return;

    if (recognition) {
        recognition.onend = null;
        recognition.stop();
    }

    isRecording = false;
    currentIndex = -1;

    document.getElementById('status').textContent = "Status: Stopped";
    toggleButtons(id, false);

    let userWord = document.getElementById(`result-${id}`).textContent.trim().toLowerCase();

    // Gửi dữ liệu lên server
    fetch('/check_word', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ word: userWord, id: id })  // Truyền đúng id
    })
        .then(response => response.json())
        .then(data => {
            console.log('Response from server:', data); // In ra dữ liệu phản hồi từ server

            if (data.correct) {
                showSuccessEffect(id);  // Hiển thị hiệu ứng thành công
            } else {
                showErrorEffect(id, data);  // Hiển thị hiệu ứng lỗi
            }
        })
        .catch(error => {
            console.error('Error:', error);  // In lỗi từ server
        });
}

function toggleButtons(id, recording) {
    const recordButton = document.querySelector(`.vocab-item button[onclick="startRecording(${id})"]`);
    const stopButton = document.querySelector(`.vocab-item button[onclick="stopRecording(${id})"]`);

    if (recordButton && stopButton) {
        recordButton.disabled = recording;  // Disable Record button
        stopButton.disabled = !recording;   // Enable Stop button
    }
}

function showSuccessEffect(id) {
    const container = document.getElementById(`result-${id}`);
    container.style.color = '#28a745';  // Màu xanh lá
    const audio = new Audio('/static/sound/correct-sound.mp3');
    audio.play();
}

function showErrorEffect(id, data) {
    const container = document.getElementById(`result-${id}`);
    container.style.color = '#dc3545';  // Màu đỏ
    const audio = new Audio('/static/sound/incorrect-sound.mp3');
    audio.play();
}

function submitAnswers() {
    const form = document.getElementById('quiz-form');
    const formData = new FormData(form);
    const answers = Object.fromEntries(formData);

    fetch('/check_answers', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(answers)
    })
    .then(response => response.json())
    .then(data => {
        const resultDiv = document.getElementById('result');
        resultDiv.innerHTML = data.correct 
            ? '<p style="color:green">All answers are correct!</p>'
            : `<p style="color:red">You got ${data.score} out of ${data.total} correct.</p>`;
        
        Object.entries(data.details).forEach(([questionId, correct]) => {
            const questionDiv = document.querySelector(`[name="question-${questionId}"]`).closest('.question-item');
            questionDiv.style.backgroundColor = correct ? '#d4edda' : '#f8d7da';
        });
    })
    .catch(error => console.error('Error:', error));
}
