let mediaRecorder;
let audioChunks = [];

//3. Mp3 to text
const uploadButton = document.getElementById('upload-button');
const fileInput = document.getElementById('file-input');
const status = document.getElementById('status');
const textOutput = document.getElementById('text-output');
const audioPlayer = document.getElementById('audio-player');
const audioSource = document.getElementById('audio-source');

// Xử lý sự kiện tải lên file và chuyển đổi
uploadButton.addEventListener('click', async () => {
    const file = fileInput.files[0];
    if (!file) {
        alert("Please select an MP3 file.");
        return;
    }

    const formData = new FormData();
    formData.append('audio', file);

    try {
        // Thông báo trạng thái tải lên
        status.textContent = "Status: Uploading file...";

        // Gửi file MP3 lên server
        const response = await fetch('/mp3-to-text', {
            method: 'POST',
            body: formData,
        });

        // Kiểm tra phản hồi từ server
        if (!response.ok) {
            const errorData = await response.json();
            alert(`Error: ${errorData.error}`);
            return;
        }

        // Nhận dữ liệu từ server
        const data = await response.json();
        textOutput.textContent = data.text || 'No text detected';
        status.textContent = "Status: File uploaded successfully";

        // Tạo URL từ file MP3 và set vào audio player để phát âm thanh
        const audioUrl = URL.createObjectURL(file);
        audioSource.src = audioUrl;

        // Hiển thị audio player và thử phát âm thanh
        audioPlayer.style.display = 'block';
        audioPlayer.load(); // Đảm bảo rằng âm thanh được tải lại

        // Thử phát âm thanh
        try {
            await audioPlayer.play();
            console.log("Audio is playing");
        } catch (err) {
            console.error("Audio playback error:", err);
            status.textContent = "Status: Audio playback failed";
        }

    } catch (error) {
        alert(`Unexpected error: ${error.message}`);
    } finally {
        status.textContent = "Status: Idle";
    }
});

function previewImage(event) {
  var reader = new FileReader();
  reader.onload = function () {
    var output = document.getElementById('avatarPreview');
    output.src = reader.result;
  };
  reader.readAsDataURL(event.target.files[0]);
}
