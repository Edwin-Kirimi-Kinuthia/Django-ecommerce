from django.contrib import admin
from .models import *



class ProductImagesInline(admin.TabularInline):
    model = ProductImages
    extra = 1


class ProductVariationInline(admin.TabularInline):
    model = ProductVariation
    extra = 1


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


class BundleItemInline(admin.TabularInline):
    model = BundleItem
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['cid', 'category_title', 'display_category_image']
    search_fields = ['category_title']


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ['scid', 'subcategory_title', 'category', 'display_subcategory_image']
    list_filter = ['category']
    search_fields = ['subcategory_title']


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ['vid', 'vendor_title', 'user', 'status', 'rating', 'display_vendor_image']
    list_filter = ['status']
    search_fields = ['vendor_title', 'user__username']


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['pid', 'product_title', 'category', 'vendor', 'discounted_price', 'normal_price', 'product_status', 'in_stock', 'display_product_image']
    list_filter = ['product_status', 'in_stock', 'featured', 'digital_product', 'category', 'vendor']
    search_fields = ['product_title', 'description']
    readonly_fields = ['date_added', 'updated', 'total_revenue', 'sold_count']
    inlines = [ProductImagesInline, ProductVariationInline]


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['cid', 'user', 'created_at', 'updated_at', 'total']
    search_fields = ['cid', 'user__username']
    inlines = [CartItemInline]


@admin.register(ProductVariation)
class ProductVariationAdmin(admin.ModelAdmin):
    list_display = ['vid', 'product', 'size', 'color', 'material', 'price_adjustment', 'stock', 'is_active']
    list_filter = ['product', 'is_active']
    search_fields = ['vid', 'product__product_title']


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['cid', 'code', 'discount', 'is_percentage', 'valid_from', 'valid_to', 'is_active']
    list_filter = ['is_active', 'is_percentage']
    search_fields = ['cid', 'code']


@admin.register(Shipping)
class ShippingAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'estimated_days']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'user', 'full_name', 'total_amount', 'order_status', 'payment_status', 'order_date', 'estimated_delivery_date']
    list_filter = ['order_status', 'payment_status']
    search_fields = ['order_id', 'user__username', 'full_name', 'email']
    inlines = [OrderItemInline]


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['wid', 'user', 'product', 'added_date']
    list_filter = ['user']
    search_fields = ['wid', 'user__username', 'product__product_title']


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['aid', 'user', 'address_line1', 'city', 'state', 'country', 'zipcode', 'is_default']
    list_filter = ['is_default', 'country', 'state']
    search_fields = ['aid', 'user__username', 'address_line1', 'city']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['pid', 'order', 'payment_method', 'transaction_id', 'amount_paid', 'payment_date']
    list_filter = ['payment_method']
    search_fields = ['pid', 'order__order_id', 'transaction_id']


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['rid', 'product', 'user', 'rating', 'created_at']
    list_filter = ['rating']
    search_fields = ['rid', 'product__product_title', 'user__username']


@admin.register(VendorReview)
class VendorReviewAdmin(admin.ModelAdmin):
    list_display = ['rid', 'vendor', 'user', 'rating', 'created_at']
    list_filter = ['rating']
    search_fields = ['rid', 'vendor__vendor_title', 'user__username']


@admin.register(InventoryChange)
class InventoryChangeAdmin(admin.ModelAdmin):
    list_display = ['icid', 'product', 'change_amount', 'reason', 'timestamp']
    list_filter = ['product']
    search_fields = ['icid', 'product__product_title', 'reason']


@admin.register(ProductReturn)
class ReturnAdmin(admin.ModelAdmin):
    list_display = ['rid', 'order', 'product', 'quantity', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['rid', 'order__order_id', 'product__product_title']


@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ['rfid', 'order', 'amount', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['rfid', 'order__order_id']


@admin.register(ProductBundle)
class ProductBundleAdmin(admin.ModelAdmin):
    list_display = ['bid', 'name', 'discount_percentage', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['bid', 'name']
    inlines = [BundleItemInline]


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['bid', 'banner_title', 'banner_link', 'is_active', 'created_at', 'updated_at', 'display_banner_image']
    list_filter = ['is_active']
    search_fields = ['bid', 'banner_title']
