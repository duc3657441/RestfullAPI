//Tắt form đăng nhập khi nhấp ra ngoài form
function showLoginForm() {
    document.getElementById('loginFormWrapper').style.display = 'flex';
}
function hideLoginForm(event) {
    if (event.target.id === 'loginFormWrapper') {
        document.getElementById('loginFormWrapper').style.display = 'none';
    }
}
function hienthiformdangki() {
    document.getElementById('loginFormWrapper').style.display = 'none';
    showRegisterForm();
}
// Kiểm tra token trong localStorage
function checkToken() {
    const token = localStorage.getItem('token');
    if (!token) {
        // Nếu không có token, chuyển hướng về trang chủ
        window.location.href = '/Home/home.html'; // Thay 'home.html' bằng đường dẫn tới trang chủ của bạn
    }
}
function hienthiformdangnhap() {
    document.getElementById('registerFormWrapper').style.display = 'none';
    showLoginForm();
}
function showRegisterForm() {
    document.getElementById('registerFormWrapper').style.display = 'flex';
}

function hideRegisterForm(event) {
    if (event.target.id === 'registerFormWrapper') {
        document.getElementById('registerFormWrapper').style.display = 'none';
    }
}
// Hàm để thêm sách vào giỏ hàng
async function addToCart(bookId) {
    const token = localStorage.getItem('token');
    
    if (!token) {
        alert('Bạn chưa đăng nhập');
        return;
    }

    try {
        const response = await fetch('http://127.0.0.1:5000/cart/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ book_id: bookId, quantity: 1 })
        });

        const data = await response.json();

        if (response.ok) {
            alert('Sách đã được thêm vào giỏ hàng:', data);
        } else {
            console.error('Lỗi thêm sách vào giỏ hàng:', data.error || 'Lỗi không xác định');
        }
    } catch (error) {
        console.error('Lỗi mạng hoặc lỗi không xác định:', error);
    }
}
function logout() {
    localStorage.removeItem('token'); // Xóa token khỏi localStorage
    alert('Đăng xuất thành công!'); // Thông báo đăng xuất thành công
    updateLoginStatus(); // Cập nhật trạng thái đăng nhập
    location.reload();       
}
function updateLoginStatus() {
    //check token
    const token = localStorage.getItem('token');
    const loginLink = document.querySelector('.login-link');
    const profile = document.getElementById('profile');
    if (token) {
        loginLink.textContent = 'Log Out';
        loginLink.onclick = logout;
        profile.style.display = 'flex';
    }
    else{
        loginLink.textContent = 'Log In';
        loginLink.onclick = showLoginForm;
        profile.style.display = 'none';
    }
}
// Hàm định dạng tiền tệ
function formatCurrency(value) {
    return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(value);
}

document.addEventListener('DOMContentLoaded', function(){
    updateLoginStatus();
});

async function login() {
    const email = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const errorMessageElement = document.getElementById('error-message');
    const notificationElement = document.getElementById('notification');
    errorMessageElement.innerText = ''; // Xóa thông báo lỗi trước đó
    notificationElement.innerText = ''; // Xóa thông báo trước đó
    try {
        const response = await fetch('http://127.0.0.1:5000/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': 'http://127.0.0.1:5000',
                'Access-Control-Allow-Credentials': 'true'
            },
            body: JSON.stringify({ 'email': email, 'password': password })
        });

        const data = await response.json();

        if (response.ok) {
            alert('Đăng nhập thành công! Token: ');
            // Lưu token vào localStorage hoặc thực hiện hành động khác
            localStorage.setItem('token', data.access_token);  
            location.reload();       
        } else {
            //  errorMessageElement.innerText = data.error;
            errorMessageElement.innerText = data.message;
        }
    } catch (error) {
        errorMessageElement.innerText = 'Có lỗi xảy ra. Vui lòng thử lại.';
    }
}


async function register() {
    const name = document.getElementById('registerUsername').value;
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;
    const errorMessageElement = document.getElementById('register-error-message');
    const notificationElement = document.getElementById('register-notification');
    errorMessageElement.innerText = ''; // Xóa thông báo lỗi trước đó
    notificationElement.innerText = ''; // Xóa thông báo trước đó

    try {
        const response = await fetch('http://127.0.0.1:5000/auth/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name, email, password })
        });

        const data = await response.json();

        if (response.ok) {
            notificationElement.innerText = 'Đăng ký thành công!';
            // Thực hiện hành động khác nếu cần
        } else {
            errorMessageElement.innerText = data.message;
            errorMessageElement.innerText += "\n" + data.error;

        }
    } catch (error) {
        errorMessageElement.innerText = 'Có lỗi xảy ra. Vui lòng thử lại.';
    }
}


async function getBooks() {
    const token = localStorage.getItem('token');
    const response = await fetch('/books/', {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });

    const data = await response.json();

    if (response.ok) {
        console.log('Books:', data);
    } else {
        console.error('Failed to get books:', data.error);
    }
}
