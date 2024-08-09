function openEditForm() {
    document.getElementById('contactInfo').style.display = 'none';
    document.getElementById('editForm').style.display = 'block';
}

function closeEditForm() {
    document.getElementById('contactInfo').style.display = 'block';
    document.getElementById('editForm').style.display = 'none';
}

document.addEventListener('DOMContentLoaded', function() {
    
    // Gọi hàm kiểm tra token khi tải trang
    checkToken();
});