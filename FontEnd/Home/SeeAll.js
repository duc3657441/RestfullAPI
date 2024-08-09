async function fetchFullProducts() {
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
        displayProducts(products);
        
    } catch (error) {
        console.error('There has been a problem with your fetch operation:', error);
    }
}
function displayProducts(products) {
    let mainContainer = document.getElementById('mainContainer'); 
    if (!mainContainer) {
        mainContainer = document.createElement('div');
        mainContainer.id = 'mainContainer';
        document.body.appendChild(mainContainer); // Hoặc thêm vào phần tử cụ thể khác trong trang
    }
    mainContainer.innerHTML = ''; // Xóa nội dung hiện tại nếu có
    for (let i = 0; i < products.length; i += 4) {
        const productGroup = products.slice(i, i + 4);

        const productContainer = document.createElement('div');
        productContainer.className = 'product-container';
        productContainer.id = `productContainer-${i / 4}`; // Đặt id duy nhất cho mỗi nhóm sản phẩm

        productGroup.forEach(product => {
          
            
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
            productPrice.innerHTML = `${formatCurrency(product.price)}`;
            productDetails.appendChild(productPrice);

            const productRating = document.createElement('div');
            productRating.className = 'rating';
            let index = 0;
            for (index; index < Math.floor(product.rating); index++) {
                productRating.textContent += '★';
            }
           
            for (i = index;index < 5;index++) {
                productRating.textContent += '☆';
                
            }
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

        mainContainer.appendChild(productContainer);
    }
    
}