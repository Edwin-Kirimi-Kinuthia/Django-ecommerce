document.addEventListener('DOMContentLoaded', function() {
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

    // Add to cart functionality
    const addToCartButtons = document.querySelectorAll('.add-to-cart');
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.dataset.productId;
            addToCart(productId);
        });
    });

    // Add to wishlist functionality
    const addToWishlistButtons = document.querySelectorAll('.add-to-wishlist');
    addToWishlistButtons.forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.dataset.productId;
            addToWishlist(productId);
        });
    });

    function addToCart(productId) {
        fetch(`/add-to-cart/${productId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert(data.message);
            } else {
                alert('Error adding product to cart');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

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
                alert(data.message);
            } else {
                alert('Error adding product to wishlist');
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
});
