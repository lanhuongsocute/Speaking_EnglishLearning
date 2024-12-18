document.addEventListener('DOMContentLoaded', () => {
    const profileButton = document.getElementById('profile-button');
    const profileDropdown = document.getElementById('profile-dropdown');

    profileButton.addEventListener('click', (e) => {
        e.stopPropagation(); // Ngăn chặn sự kiện lan ra ngoài
        profileButton.parentElement.classList.toggle('active');
    });

    // Ẩn dropdown khi click ra ngoài
    document.addEventListener('click', () => {
        profileButton.parentElement.classList.remove('active');
    });
});
