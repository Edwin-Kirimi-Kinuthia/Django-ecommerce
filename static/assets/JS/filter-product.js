$(document).ready(function() {
    const priceSlider = document.getElementById('priceSlider');
    const priceValue = document.getElementById('priceValue');
    const priceInput = document.getElementById('priceInput');
    const filterButton = document.getElementById('filterButton');
    const sortSelect = document.getElementById('sort-select');

    priceSlider.addEventListener('input', function() {
        priceValue.textContent = `${parseFloat(this.value).toFixed(2)}`;
        priceInput.value = this.value;
    });

    priceInput.addEventListener('input', function() {
        const selectedPrice = parseFloat(this.value);
        priceSlider.value = selectedPrice; 
        priceValue.textContent = `${selectedPrice.toFixed(2)}`;
    });

    $(".filter-checkbox").on("change", applyFiltersAndSort);
    $(filterButton).on('click', applyFiltersAndSort);
    $(sortSelect).on('change', applyFiltersAndSort);

    $(document).on('click', '#pagination .page-link', function(e) {
        e.preventDefault();
        const pageNumber = $(this).data('page');
        applyFiltersAndSort(pageNumber);
    });

    function applyFiltersAndSort(page = 1) {
        let filterData = getFilterParameters();
        if (typeof page === 'object') {
            page = 1;  // Reset to first page when filters change
        }
        filterData.page = page;
        filterData.sort = $(sortSelect).val();

        $.ajax({
            url: '/filter-and-sort-products/',
            data: filterData,
            dataType: 'json',
            success: function(response) {
                $("#filtered-products").html(response.data);
                $("#pagination").html(response.pagination);
            },
            error: function(xhr, status, error) {
                console.error("Error applying filters and sorting:", error);
            }
        });
    }

    function getFilterParameters() {
        let filterData = {};

        $(".filter-checkbox:checked").each(function(){
            let filterValue = $(this).val();
            let filterKey = $(this).data("filter");
            
            if (!filterData[filterKey]) {
                filterData[filterKey] = [];
            }
            filterData[filterKey].push(filterValue);
        });

        const selectedPrice = parseFloat(priceInput.value);
        filterData.price = selectedPrice;

        return filterData;
    }
});