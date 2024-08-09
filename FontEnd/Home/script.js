function layNgauNhienSP(arr) {
    // Tạo một bản sao của mảng để tránh ảnh hưởng đến mảng gốc
    let shuffled = arr.slice(0);
    
    // xáo trộn mảng đã sao chép
    for (let i = shuffled.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }
    return shuffled;
}
 // Hàm hiển thị sản phẩm lên trang web
 function displayProducts(products, count) {
    
    const productContainer = document.getElementById('productContainer');
    
    productContainer.innerHTML = ''; // Xóa nội dung hiện tại nếu có
    let randomProducts = products;
    if (count == '4') {
        randomProducts  = layNgauNhienSP(products).slice(0,4);
    }
    
    randomProducts.forEach(product => {
        
        
        const productCard = document.createElement('div');
        productCard.className = 'product-card';

        const saleBadge = document.createElement('div');
        saleBadge.className = 'sale-badge';
        saleBadge.textContent = 'SALE';
        productCard.appendChild(saleBadge);

        const productImage = document.createElement('img');
        productImage.src = product.image_url;
        
        productImage.alt = product.title;
        productCard.appendChild(productImage);

        const productDetails = document.createElement('div');
        productDetails.className = 'product-details';

        const productName = document.createElement('h4');
        productName.textContent = product.title;
        productDetails.appendChild(productName);

        const productPrice = document.createElement('div');
        productPrice.className = 'price';
        const price = product.price;
        productPrice.innerHTML = price;
        productDetails.appendChild(productPrice);

        const productRating = document.createElement('div');
        productRating.className = 'rating';
        let index = 0
        for (index ; index < product.rating; index++) {
            productRating.textContent += '★';
        }
        if (index - 1 < product.rating < index) {
            productRating.textContent += '★';
        }
        // Assuming rating is a string like '★★★☆☆'
        productDetails.appendChild(productRating);

        const productCategory = document.createElement('div');
        productCategory.className = 'category';
        productCategory.textContent = product.category;
        productDetails.appendChild(productCategory);

        const addToCartButton = document.createElement('button');
        addToCartButton.className = 'add-to-cart';
        addToCartButton.textContent = 'Add to cart';
        addToCartButton.addEventListener('click', () => addToCart(product.id));
        productDetails.appendChild(addToCartButton);

        productCard.appendChild(productDetails);
        productContainer.appendChild(productCard);
       
    });
}

async function fetchProducts() {
    try {
        const response = await fetch('http://127.0.0.1:5000/books/', {
            method: 'GET',
            headers: {
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Credentials': 'true'
                    },
                    });
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const products = await response.json();
        displayProducts(products,'4');
        
    } catch (error) {
        console.error('There has been a problem with your fetch operation:', error);
    }
}






