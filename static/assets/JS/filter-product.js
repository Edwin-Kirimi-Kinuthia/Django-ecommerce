$(document).ready(function(){
    // Existing price slider logic
    const priceSlider = document.getElementById('priceSlider');
    const priceValue = document.getElementById('priceValue');
    const priceInput = document.getElementById('priceInput');
    const filterButton = document.getElementById('filterButton');

    // Updates the displayed price and input field when the slider is moved
    priceSlider.addEventListener('input', function() {
        priceValue.textContent = `${parseFloat(this.value).toFixed(2)}`;
        priceInput.value = this.value;
    });

    // Syncs the slider with the input price when the user types in the input field
    priceInput.addEventListener('input', function() {
        const selectedPrice = parseFloat(this.value);
        priceSlider.value = selectedPrice; 
        priceValue.textContent = `${selectedPrice.toFixed(2)}`; 
    });

    // Function to apply filters
    function applyFilters() {
        let filter_object = {};
        
        // Collect category and vendor filters
        $(".filter-checkbox:checked").each(function(){
            let filter_value = $(this).val();
            let filter_key = $(this).data("filter");
            
            if (!filter_object[filter_key]) {
                filter_object[filter_key] = [];
            }
            filter_object[filter_key].push(filter_value);
        });

        // Add price filter
        const selectedPrice = parseFloat(priceInput.value);
        filter_object['price'] = selectedPrice;

        // AJAX call to filter products
        $.ajax({
            url: 'filter-products/',
            data: filter_object,
            dataType: 'json',
            success: function(response){
                $("#filtered-products").html(response.data);
            },
            error: function(xhr, status, error) {
                console.error("Error applying filters:", error);
            }
        });
    }

    // Event listener for checkbox filters
    $(".filter-checkbox").on("click", applyFilters);

    // Event listener for price filter button
    filterButton.addEventListener('click', function() {
        const selectedPrice = parseFloat(priceInput.value);
        const minPrice = parseFloat(priceInput.min);
        const maxPrice = parseFloat(priceInput.max);

        if (selectedPrice < minPrice || selectedPrice > maxPrice) {
            alert(`Price must be between ${minPrice.toFixed(2)} and ${maxPrice.toFixed(2)}.`);
            priceInput.value = minPrice;
            priceSlider.value = minPrice;
            priceValue.textContent = `${minPrice.toFixed(2)}`;
            priceInput.focus();
        } else {
            applyFilters();
        }
    });
});