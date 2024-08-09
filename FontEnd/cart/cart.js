document.addEventListener('DOMContentLoaded', async () => {
    await loadCart();
});

async function loadCart() {
    const token = localStorage.getItem('token');

    if (!token) {
        alert('Token không tồn tại');
        return;
    }

    try {
        const response = await fetch('http://127.0.0.1:5000/cart/', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        const data = await response.json();

        if (response.ok) {
            renderCart(data);
        } else {
            console.error('Lỗi lấy giỏ hàng:', data.error || 'Lỗi không xác định');
        }
    } catch (error) {
        console.error('Lỗi mạng hoặc lỗi không xác định:', error);
    }
}

function renderCart(cart) {
    const cartItemsContainer = document.getElementById('cart-items');
    const totalPriceElement = document.getElementById('total-price');

    cartItemsContainer.innerHTML = ''; // Xóa nội dung cũ

    let totalPrice = 0;

    cart.items.forEach(item => {
        const itemElement = document.createElement('div');
        itemElement.className = 'cart-item';
        itemElement.innerHTML = `
            <div class="sale-badge">SALE</div>
            <img src="${item.book_image}" alt="${item.book_title}">
            <div class="item-details">
                <h4>${item.book_title}</h4>
                <p>$${item.book_price} x ${item.quantity}</p>
            </div>
            <div class="item-total">
                $${(item.book_price * item.quantity).toFixed(2)}
            </div>
        `;
        cartItemsContainer.appendChild(itemElement);
        totalPrice += item.book_price * item.quantity;
    });

    totalPriceElement.textContent = totalPrice.toFixed(2);
}

async function checkout() {
    // Hiển thị hộp thoại xác nhận phương thức thanh toán
    document.getElementById('payment-dialog').style.display = 'flex';
}

function closePaymentDialog() {
    document.getElementById('payment-dialog').style.display = 'none';
}

function handlePayment(method) {
    // Đóng hộp thoại
    closePaymentDialog();

    // Hiển thị hộp thoại xác nhận thanh toán
    const isConfirmed = confirm(`Bạn chọn thanh toán bằng ${method === 'cash' ? 'tiền mặt' : 'thẻ/ ví trả sau'}. Bạn có chắc chắn muốn tiếp tục không?`);

    if (!isConfirmed) {
        return; // Nếu người dùng hủy, không thực hiện thanh toán
    }

    processPayment(method);
}

async function processPayment(method) {
    const token = localStorage.getItem('token');

    if (!token) {
        console.error('Token không tồn tại');
        return;
    }

    try {
        const response = await fetch('http://127.0.0.1:5000/cart/checkout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ payment_method: method })
        });

        const data = await response.json();

        if (response.ok) {
            // Chuyển hướng đến trang thanh toán thành công
            window.location.href = 'success.html'; // Thay đổi đường dẫn nếu cần thiết
        } else {
            console.error('Lỗi thanh toán:', data.error || 'Lỗi không xác định');
        }
    } catch (error) {
        console.error('Lỗi mạng hoặc lỗi không xác định:', error);
    }
}
