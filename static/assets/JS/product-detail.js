document.addEventListener('DOMContentLoaded', function() {
    // Image handling
    const mainImage = document.getElementById('main-image');
    const mainImageContainer = document.querySelector('.main-image-container');
    const thumbnails = document.querySelectorAll('.thumbnail');
    const thumbnailsContainer = document.querySelector('.thumbnails');
    
    let isZoomed = false;
    let zoomLevel = 2.5;

    // Thumbnail click event
    thumbnails.forEach(thumbnail => {
        thumbnail.addEventListener('click', function() {
            mainImage.src = this.dataset.src;
            thumbnails.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
        });
    });

    // Zoom functionality
    mainImageContainer.addEventListener('mouseenter', function() {
        isZoomed = true;
        mainImage.style.transition = 'transform 0.3s ease';
    });

    mainImageContainer.addEventListener('mousemove', function(e) {
        if (isZoomed) {
            const rect = mainImageContainer.getBoundingClientRect();
            const x = (e.clientX - rect.left) / rect.width;
            const y = (e.clientY - rect.top) / rect.height;

            mainImage.style.transformOrigin = `${x * 100}% ${y * 100}%`;
            mainImage.style.transform = `scale(${zoomLevel})`;
        }
    });

    mainImageContainer.addEventListener('mouseleave', function() {
        isZoomed = false;
        mainImage.style.transform = 'scale(1)';
    });

    // Thumbnail scroll functionality
    let scrollPosition = 0;
    const scrollStep = 70; // Adjust based on thumbnail width + margin

    function scrollThumbnails(direction) {
        const maxScroll = thumbnailsContainer.scrollWidth - thumbnailsContainer.clientWidth;
        if (direction === 'left') {
            scrollPosition = Math.max(scrollPosition - scrollStep, 0);
        } else {
            scrollPosition = Math.min(scrollPosition + scrollStep, maxScroll);
        }
        thumbnailsContainer.style.transform = `translateX(-${scrollPosition}px)`;
    }

    // Add scroll buttons if needed
    const thumbnailsWrapper = document.querySelector('.thumbnails-container');
    if (thumbnailsContainer.scrollWidth > thumbnailsWrapper.clientWidth) {
        const leftButton = document.createElement('button');
        leftButton.textContent = '<';
        leftButton.classList.add('thumbnail-scroll-button', 'left');
        leftButton.addEventListener('click', () => scrollThumbnails('left'));

        const rightButton = document.createElement('button');
        rightButton.textContent = '>';
        rightButton.classList.add('thumbnail-scroll-button', 'right');
        rightButton.addEventListener('click', () => scrollThumbnails('right'));

        thumbnailsWrapper.appendChild(leftButton);
        thumbnailsWrapper.appendChild(rightButton);
    }

    // Cart functionality
    const cartCounter = document.querySelector('.cart-counter');
    const cartItemsContainer = document.getElementById('cartItems');
    const cartTotalElement = document.getElementById('cartTotal');
    const cartIcon = document.querySelector('.cart-icon');

    function updateCartDisplay(cartItems, cartTotal, cartCount) {
        cartCounter.textContent = cartCount;
        cartTotalElement.textContent = cartTotal.toFixed(2);

        cartItemsContainer.innerHTML = '';
        cartItems.forEach(item => {
            const itemElement = document.createElement('div');
            itemElement.className = 'cart-item';
            itemElement.innerHTML = `
                <span>${item.product__product_title} x ${item.quantity}</span>
                <span>$${item.total_price.toFixed(2)}</span>
            `;
            cartItemsContainer.appendChild(itemElement);
        });
    }

    function fetchCartItems() {
        fetch('/get-cart-items/', {
            method: 'GET',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                updateCartDisplay(data.cart_items, data.cart_total, data.cart_count);
            } else {
                showNotification('Error fetching cart items', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('An error occurred', 'error');
        });
    }

    // Fetch cart items on page load
    fetchCartItems();

    // Add to cart functionality
    const addToCartButtons = document.querySelectorAll('.add-to-cart');
    const quantityInputs = document.querySelectorAll('.quantity-input');

    addToCartButtons.forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.dataset.productId;
            const productName = this.dataset.productName;
            const productPrice = this.dataset.productPrice;
            const quantityInput = this.closest('.add-to-cart-container').querySelector('.quantity-input');
            const quantity = parseInt(quantityInput.value);
            addToCart(productId, productName, productPrice, quantity);
        });
    });

    quantityInputs.forEach(input => {
        input.addEventListener('input', function() {
            const max = parseInt(this.max);
            const value = parseInt(this.value);
            if (value > max) {
                this.value = max;
            }
            if (value < 1) {
                this.value = 1;
            }
        });
    });


    function addToCart(productId, productName, productPrice, quantity) {
        fetch(`/add-to-cart/${productId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                quantity: quantity,
                product_name: productName,
                product_price: productPrice
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                showNotification(`Added ${quantity} x ${productName} to cart`, 'success');
                updateCartDisplay(data.cart_items, data.cart_total, data.cart_count);
            } else {
                showNotification('Error adding product to cart', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('An error occurred', 'error');
        });
    }

    // Add to wishlist functionality
    const addToWishlistButtons = document.querySelectorAll('.add-to-wishlist');
    addToWishlistButtons.forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.dataset.productId;
            addToWishlist(productId);
        });
    });

    function addToWishlist(productId) {
        fetch(`/add-to-wishlist/${productId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success' || data.status === 'info') {
                showNotification(data.message, 'success');
            } else {
                showNotification('Error adding product to wishlist', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('An error occurred', 'error');
        });
    }

    function showNotification(message, type) {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        document.body.appendChild(notification);

        // Trigger reflow
        notification.offsetHeight;

        notification.classList.add('show');

        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 3000);
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});