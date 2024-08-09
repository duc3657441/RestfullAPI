document.getElementById('addBookForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    // Lấy giá trị từ form
    const imageFile = document.getElementById('bookImage').files[0];
    const reader = new FileReader();
    reader.onload = function(event) {
        const image = event.target.result;
        const title = document.getElementById('bookTitle').value;
        const author = document.getElementById('bookAuthor').value;
        const genre = document.getElementById('bookGenre').value;
        const year = document.getElementById('bookYear').value;
        const price = document.getElementById('bookPrice').value;
        const description = document.getElementById('bookDescription').value;

        // Thêm sách vào danh sách
        addBookToList(image, title, author, genre, year, price, description);

        // Xóa form
        document.getElementById('addBookForm').reset();
        
        // Ẩn form sau khi thêm sách
        closeForm();
    }
    reader.readAsDataURL(imageFile);
});

function addBookToList(image, title, author, genre, year, price, description) {
    const bookList = document.getElementById('bookList');
    const row = document.createElement('tr');

    row.innerHTML = `
        <td><img src="${image}" alt="${title}" style="width: 100px; height: auto;"></td>
        <td>${title}</td>
        <td>${author}</td>
        <td>${genre}</td>
        <td>${year}</td>
        <td>${price}</td>
        <td>${description}</td>
        <td>
            <button onclick="editBook(this)">Sửa</button>
            <button onclick="removeBook(this)">Xóa</button>
        </td>
    `;

    bookList.appendChild(row);
}

function removeBook(button) {
    const row = button.parentElement.parentElement;
    row.remove();
}

function openForm() {
    document.getElementById('bookFormModal').style.display = 'block';
}

function closeForm() {
    document.getElementById('bookFormModal').style.display = 'none';
}

function openEditForm() {
    document.getElementById('editBookFormModal').style.display = 'block';
}

function closeEditForm() {
    document.getElementById('editBookFormModal').style.display = 'none';
}

function editBook(button) {
    const row = button.parentElement.parentElement;
    const cells = row.getElementsByTagName('td');

    const image = cells[0].getElementsByTagName('img')[0].src;
    const title = cells[1].innerText;
    const author = cells[2].innerText;
    const genre = cells[3].innerText;
    const year = cells[4].innerText;
    const price = cells[5].innerText;
    const description = cells[6].innerText;

    document.getElementById('editBookTitle').value = title;
    document.getElementById('editBookAuthor').value = author;
    document.getElementById('editBookGenre').value = genre;
    document.getElementById('editBookYear').value = year;
    document.getElementById('editBookPrice').value = price;
    document.getElementById('editBookDescription').value = description;

    document.getElementById('editBookForm').onsubmit = function(event) {
        event.preventDefault();

        cells[1].innerText = document.getElementById('editBookTitle').value;
        cells[2].innerText = document.getElementById('editBookAuthor').value;
        cells[3].innerText = document.getElementById('editBookGenre').value;
        cells[4].innerText = document.getElementById('editBookYear').value;
        cells[5].innerText = document.getElementById('editBookPrice').value;
        cells[6].innerText = document.getElementById('editBookDescription').value;

        const newImageFile = document.getElementById('editBookImage').files[0];
        if (newImageFile) {
            const reader = new FileReader();
            reader.onload = function(event) {
                cells[0].getElementsByTagName('img')[0].src = event.target.result;
            }
            reader.readAsDataURL(newImageFile);
        }

        closeEditForm();
    }

    openEditForm();
}

// Đóng modal khi nhấn vào bên ngoài modal
window.onclick = function(event) {
    const addModal = document.getElementById('bookFormModal');
    const editModal = document.getElementById('editBookFormModal');
    if (event.target === addModal) {
        addModal.style.display = "none";
    }
    if (event.target === editModal) {
        editModal.style.display = "none";
    }
}
