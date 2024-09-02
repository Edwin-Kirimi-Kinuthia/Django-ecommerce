document.addEventListener('DOMContentLoaded', function() {
    const cartCounter = document.querySelector('.cart-counter');

    function updateCartCounter(count) {
        cartCounter.textContent = count;
        cartCounter.style.display = count > 0 ? 'inline' : 'none';
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
                updateCartCounter(data.cart_count);
            } else {
                console.error('Error fetching cart items');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
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

    // Fetch cart items on page load
    fetchCartItems();

    // Listen for custom event when cart is updated
    document.addEventListener('cartUpdated', function(e) {
        updateCartCounter(e.detail.cartCount);
    });
});