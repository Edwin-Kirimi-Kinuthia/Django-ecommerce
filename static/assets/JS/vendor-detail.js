// vendor-detail.js

document.addEventListener('DOMContentLoaded', function() {
    const starRatings = document.querySelectorAll('.star-rating');
    
    starRatings.forEach(function(starRating) {
        const rating = parseFloat(starRating.getAttribute('data-rating'));
        const fullStars = Math.floor(rating);
        const halfStar = rating % 1 >= 0.5;
        
        let stars = '⭐'.repeat(fullStars);
        if (halfStar) {
            stars += '⭐';
        }
        stars += '✰'.repeat(5 - Math.ceil(rating));
        
        starRating.textContent = stars;
    });
});