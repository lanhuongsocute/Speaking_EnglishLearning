let recognition;
let isRecording = false;
let transcript = "";

// Bắt đầu ghi âm
document.getElementById("start-recording").addEventListener("click", () => {
    recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'en-US';
    recognition.interimResults = true;

    recognition.onresult = (event) => {
        transcript = "";
        for (let i = event.resultIndex; i < event.results.length; i++) {
            if (event.results[i].isFinal) {
                transcript += event.results[i][0].transcript;
            }
        }
        document.getElementById("transcript").textContent = transcript;
    };

    recognition.start();
    isRecording = true;
    document.getElementById("start-recording").disabled = true;
    document.getElementById("stop-recording").disabled = false;
});

// Dừng ghi âm
document.getElementById("stop-recording").addEventListener("click", () => {
    if (isRecording) {
        recognition.stop();
        isRecording = false;
        document.getElementById("start-recording").disabled = false;
        document.getElementById("stop-recording").disabled = true;
        document.getElementById("save-answer").disabled = false;
    }
});

// Lưu câu trả lời
document.getElementById('save-answer').addEventListener('click', async () => {
    const question = document.getElementById('question-content').textContent;
    const answer = document.getElementById('answer-content').value.trim();

    if (!answer) {
        alert('Please provide an answer before saving.');
        return;
    }

    try {
        const response = await fetch('/save_answer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question, answer }),
        });

        const data = await response.json();

        if (response.ok && data.message === 'Answer saved successfully!') {
            alert('Answer saved successfully!');
            // Hiển thị link tải file
            const downloadLink = document.getElementById('download-link');
            downloadLink.href = `/${data.file_path}`; // Đường dẫn file
            downloadLink.style.display = 'inline'; // Hiển thị thẻ `<a>`
        } else {
            alert(data.message || 'Failed to save the answer. Please try again.');
        }
    } catch (error) {
        console.error('Error saving answer:', error);
        alert('An error occurred. Please try again.');
    }
});



