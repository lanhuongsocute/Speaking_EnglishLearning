
$('#menu-toggle').click(function () {
    $('#sidebar').toggleClass('active');
    $('#page-content-wrapper').toggleClass('active');
});

document.addEventListener("DOMContentLoaded", function () {
    const toggleLinks = document.querySelectorAll(".toggle-menu");

    toggleLinks.forEach(link => {
        link.addEventListener("click", function (event) {
            event.preventDefault();

            // Ẩn tất cả các menu con trước
            document.querySelectorAll(".submenu").forEach(submenu => {
                submenu.style.display = "none";
            });

            // Hiển thị menu con liên quan
            const target = document.querySelector(this.dataset.target);
            if (target) {
                target.style.display = "block";
            }
        });
    });
});


//------------------------------------------
document.querySelectorAll('.delete-btn').forEach(button => {
    button.addEventListener('click', function () {
        const topicId = this.getAttribute('data-id');
        if (confirm('Bạn có chắc chắn muốn xóa chủ đề này?')) {
            fetch(`/delete_topic/${topicId}`, {
                method: 'DELETE',  // Phương thức DELETE
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': '{{ csrf_token() }}'  // Thêm CSRF token nếu sử dụng Flask
                }
            })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        document.getElementById(`topic-${topicId}`).remove(); // Xóa row trong bảng
                        alert(data.message); // Hiển thị thông báo thành công
                    } else {
                        alert(data.message); // Hiển thị thông báo lỗi
                    }
                })
                .catch(error => {
                    console.error('Lỗi khi xóa chủ đề:', error);
                    alert('Đã xảy ra lỗi, vui lòng thử lại.');
                });
        }
    });
});


function toggleFormFields() {
    const lessonType = document.getElementById('lesson_type').value;
    if (lessonType === 'vocabulary') {
        document.getElementById('vocabulary_fields').style.display = 'block';
        document.getElementById('normal_fields').style.display = 'none';
    } else {
        document.getElementById('vocabulary_fields').style.display = 'none';
        document.getElementById('normal_fields').style.display = 'block';
    }
}

function addChoiceField() {
    const container = document.getElementById('choices-container');
    const choiceCount = container.children.length;  // Đếm số lượng choice hiện tại
    const choiceField = `
        <div class="choice-item">
            <input type="text" name="choices[]" placeholder="Value" required>
            <input type="radio" name="correct_choice" value="${choiceCount}"> Correct Answer
            <button type="button" onclick="this.parentElement.remove()">Delete</button>
        </div>
    `;
    container.insertAdjacentHTML('beforeend', choiceField);
}