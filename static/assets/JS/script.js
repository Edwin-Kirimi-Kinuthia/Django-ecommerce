document.addEventListener('DOMContentLoaded', function() {
    const cartCounter = document.querySelector('.cart-counter');
    const cartItemsContainer = document.getElementById('cartItems');
    const cartTotalElement = document.getElementById('cartTotal');
    const cartDropdown = document.querySelector('.cart-dropdown');

    // Function to update the cart display in the dropdown
    function updateCartDisplay(cartItems, cartTotal, cartCount) {
        cartCounter.textContent = cartCount;
        cartCounter.style.display = cartCount > 0 ? 'inline' : 'none';
        cartTotalElement.textContent = `sh.${cartTotal.toFixed(2)}`;

        cartItemsContainer.innerHTML = ''; // Clear the cart items container
        if (cartItems.length === 0) {
            cartItemsContainer.innerHTML = '<p class="text-muted text-center">Your cart is empty</p>';
            return;
        }

        cartItems.forEach(item => {
            const itemElement = document.createElement('div');
            itemElement.className = 'cart-item d-flex justify-content-between align-items-center';
            itemElement.innerHTML = `
                <div class="cart-item-info d-flex align-items-center">
                    <img src="${item.product__product_image_url}" alt="${item.product__product_title}" width="50" height="50" class="me-2">
                    <span class="item-title">${item.product__product_title}</span>
                </div>
                <div class="cart-item-controls d-flex align-items-center">
                    <input type="number" class="form-control quantity-input me-2" value="${item.quantity}" min="1" data-item-id="${item.id}">
                    <button class="btn btn-sm btn-danger remove-cart-item me-2" data-item-id="${item.id}">
                        <i class="bi bi-trash"></i>
                    </button>
                    <span class="item-price">sh.${Number(item.total_price).toFixed(2)}</span>
                </div>
            `;
            cartItemsContainer.appendChild(itemElement);
        });

        addQuantityUpdateListeners();
        addRemoveItemListeners();
    }

    // Fetch cart items from the server
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
                console.error('Error fetching cart items:', data.message);
            }
        })
        .catch(error => {
            console.error('Error fetching cart items:', error);
        });
    }

    // Function to update cart item quantity
    function updateCartItemQuantity(itemId, newQuantity) {
        fetch(`/update-cart-item/${itemId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ quantity: newQuantity })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                fetchCartItems();
            } else {
                console.error('Error updating cart item:', data.message);
            }
        })
        .catch(error => {
            console.error('Error updating cart item:', error);
        });
    }

    // Function to remove a cart item
    function removeCartItem(itemId) {
        fetch(`/remove-cart-item/${itemId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                fetchCartItems();
            } else {
                console.error('Error removing cart item:', data.message);
            }
        })
        .catch(error => {
            console.error('Error removing cart item:', error);
        });
    }

    // Add event listeners to update quantity when input changes
    function addQuantityUpdateListeners() {
        document.querySelectorAll('.quantity-input').forEach(input => {
            input.addEventListener('change', function(e) {
                e.stopPropagation(); // Prevent event from bubbling up
                const itemId = this.dataset.itemId;
                const newQuantity = parseInt(this.value);
                if (newQuantity > 0) {
                    updateCartItemQuantity(itemId, newQuantity);
                } else {
                    this.value = 1; // Set the quantity back to 1 if the user tries to set it below 1
                }
            });
        });
    }

    // Add event listeners to remove items when the trash icon is clicked
    function addRemoveItemListeners() {
        document.querySelectorAll('.remove-cart-item').forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault(); // Prevent default button action
                e.stopPropagation(); // Prevent event from bubbling up
                const itemId = this.dataset.itemId;
                removeCartItem(itemId);
            });
        });
    }

    // Helper function to get CSRF token
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

    // Fetch cart items on page load
    fetchCartItems();

    // Prevent dropdown from closing when clicking inside
    if (cartDropdown) {
        cartDropdown.addEventListener('click', function(e) {
            e.stopPropagation();
        });
    }
});
