from django.urls import path
from core import views

app_name = "core"

urlpatterns = [
    #Homepage
    path('', views.index, name="index" ),
    #Search querry
    path('search/', views.search_view, name='search'),
    #All products
    path('products', views.product_list_view, name="product-list" ),
    #Categories
    path('categories/', views.category_list, name='category-list'),
    #Subcategories
    path('category/<str:cid>/', views.subcategory_list, name='subcategory-list'),
    #products by subcategories
    path('subcategory/<str:scid>/products/', views.product_by_subcategory, name='product-by-subcategory'),
    #Vendor detail page
    path('vendor/<str:vid>/', views.vendor_detail, name='vendor-detail'),
    #Tags
    path('tag/<slug:tag_slug>/', views.tag_products, name='tag-products'),
    #Product detail
    path('product/<str:pid>/', views.product_detail, name='product-detail'),
    #Cart functionalities
    path('add-to-cart/<str:pid>/', views.add_to_cart, name='add-to-cart'),
    path('get-cart-items/', views.get_cart_items, name='get-cart-items'),
    path('update-cart-item/<int:item_id>/', views.update_cart_item, name='update-cart-item'),
    path('remove-cart-item/<int:item_id>/', views.remove_cart_item, name='remove-cart-item'),
    #Add to wishlist
    path('add-to-wishlist/<str:pid>/', views.add_to_wishlist, name='add-to-wishlist'),
    #Buy now
    path('buy-now/<str:pid>/', views.buy_now, name='buy-now'),
    #Tinymce
    path('upload_image/', views.upload_image, name='upload_image'),
    # filter products and sort products
    path('filter-and-sort-products/', views.filter_and_sort_products, name='filter-and-sort-products'),
    
]
