document.addEventListener('DOMContentLoaded', async () => {
    const bookId = document.getElementById('book-id').value;
    await loadFeedback(bookId);

    document.getElementById('feedback-form').addEventListener('submit', async (event) => {
        event.preventDefault();
        const feedbackText = document.getElementById('feedback-text').value;
        await addFeedback(bookId, feedbackText);
        document.getElementById('feedback-text').value = ''; // Xóa nội dung form sau khi gửi
        await loadFeedback(bookId); // Tải lại feedback để cập nhật danh sách
    });
});

async function addFeedback(bookId, feedbackText) {
    const token = localStorage.getItem('token');

    if (!token) {
        console.error('Token không tồn tại');
        return;
    }

    try {
        const response = await fetch('http://127.0.0.1:5000/feedback/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ book_id: bookId, feedback: feedbackText })
        });

        const data = await response.json();

        if (response.ok) {
            console.log('Feedback đã được thêm:', data);
        } else {
            console.error('Lỗi thêm feedback:', data.error || 'Lỗi không xác định');
        }
    } catch (error) {
        console.error('Lỗi mạng hoặc lỗi không xác định:', error);
    }
}

async function loadFeedback(bookId) {
    const token = localStorage.getItem('token');

    if (!token) {
        console.error('Token không tồn tại');
        return;
    }

    try {
        const response = await fetch(`http://127.0.0.1:5000/feedback/book/${bookId}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        const data = await response.json();

        if (response.ok) {
            renderFeedback(data);
        } else {
            console.error('Lỗi lấy feedback:', data.error || 'Lỗi không xác định');
        }
    } catch (error) {
        console.error('Lỗi mạng hoặc lỗi không xác định:', error);
    }
}

function renderFeedback(feedbackList) {
    const feedbackListContainer = document.getElementById('feedback-list');
    feedbackListContainer.innerHTML = ''; // Xóa nội dung cũ

    feedbackList.forEach(feedback => {
        const feedbackElement = document.createElement('div');
        feedbackElement.className = 'feedback-item';
        feedbackElement.innerHTML = `
            <p><strong>${feedback.user_name}</strong>: ${feedback.feedback}</p>
        `;
        feedbackListContainer.appendChild(feedbackElement);
    });
}
