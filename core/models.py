from django.db import models
from django.utils.html import mark_safe
from userauths.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.db.models import Avg
#Third party
from shortuuid.django_fields import ShortUUIDField
from tinymce.models import HTMLField


STATUS = (
    ("draft", "Draft"),
    ("rejected", "rejected"),
    ("disabled", "Disabled"),
    ("in review", "In Review"),
    ("published", "Published"),    
)

RATING = (
    (1, "⭐✰✰✰✰"),
    (2, "⭐⭐✰✰✰"),
    (3, "⭐⭐⭐✰✰"),
    (4, "⭐⭐⭐⭐✰"),
    (5, "⭐⭐⭐⭐⭐"),   
)

def user_directory_path(instance, filename):
    model_name = instance.__class__.__name__.lower()
    return '{0}/user_{1}/{2}'.format(model_name, instance.user.id, filename)


class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="cat", alphabet="abcdefghijklmnopqrstuvwxyz1234567890")
    category_title = models.CharField(max_length=255, unique=True)
    category_image = models.ImageField(upload_to= "categories", default="category.jpg")

    class Meta:
        verbose_name_plural = "Categories"

    def display_category_image(self):
        return mark_safe('<img src="%s" width= "50" height= "50"/>' %(self.category_image.url))

    def __str__(self):
        return self.category_title


class Subcategory(models.Model):
    scid = ShortUUIDField(unique=True, length=10, max_length=30, prefix="subcat", alphabet="abcdefghijklmnopqrstuvwxyz1234567890")
    subcategory_title = models.CharField(max_length=255)
    subcategory_image = models.ImageField(upload_to= "subcategories", default="subcategory.jpg")
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Sub-categories"
        unique_together = ('subcategory_title', 'category')
    
    def display_subcategory_image(self):
        return mark_safe('<img src="%s" width= "50" height= "50"/>' %(self.subcategory_image.url))

    def __str__(self):
        return f"{self.subcategory_title} ({self.category.category_title})"


class Vendor(models.Model):
    vid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="ven", alphabet="abcdefghijklmnopqrstuvwxyz1234567890")
    vendor_title = models.CharField(max_length=255, unique=True, default="BLUST BY DR MA")
    vendor_image = models.ImageField(upload_to=user_directory_path, default="vendor.jpg")
    description = HTMLField(max_length=3067, null=True, blank=True, default="My vending shop")
    vendor_adress = models.CharField(max_length=255, default="123 Main Street")
    vendor_contact = models.CharField(max_length=255, default="+123 (456) (890)")
    vendor_chat_resp_time = models.CharField(max_length=255, default="100")
    shipping_on_time = models.CharField(max_length=255, default="100")
    authentic_rating = models.CharField(max_length=255, default="100")
    days_return = models.CharField(max_length=255, default="100")
    warranty_period = models.CharField(max_length=255, default="100")
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('inactive', 'Inactive'), ('suspended', 'Suspended')], default='active')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        verbose_name_plural = "Vendors"
    
    def display_vendor_image(self):
        return mark_safe('<img src="%s" width= "50" height= "50"/>' %(self.vendor_image.url))

    def __str__(self):
        return self.vendor_title
    
    @property
    def rating(self):
        average_rating = self.reviews.aggregate(Avg('rating'))['rating__avg']
        return round(average_rating, 2) if average_rating else 0


class Tags(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Tags"

    def __str__(self):
        return self.name


class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefghijklmnopqrstuvwxyz1234567890")
    product_title = models.CharField(max_length=255, unique=True, default="My product")
    product_image = models.ImageField(upload_to=user_directory_path, default="product.jpg")
    stock_amount = models.IntegerField(default=1, validators=[MinValueValidator(0)])
    description = HTMLField(max_length=3067, null=True, blank=True, default="This is the product")
    discounted_price = models.DecimalField(max_digits=12, decimal_places=2, default="1.99", validators=[MinValueValidator(0)])
    normal_price = models.DecimalField(max_digits=12, decimal_places=2, default="2.99", validators=[MinValueValidator(0)])
    specification = models.CharField(max_length=255, default="Organic")
    product_status = models.CharField(choices=STATUS, max_length=255, default="in review")
    is_published = models.BooleanField(default=False)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital_product = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tags, blank=True)
    sku = ShortUUIDField(unique=True, length=5, max_length=10, prefix="sku", alphabet="abcdefghijklmnopqrstuvwxyz1234567890")
    date_added = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now, blank=True, null=True)
    total_stock = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    available_stock = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    sold_count = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    last_sold_date = models.DateTimeField(null=True, blank=True)
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    low_stock_threshold = models.PositiveIntegerField(default=10, validators=[MinValueValidator(0)])
    is_low_stock = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='products')

    class Meta:
        verbose_name_plural = "Products"

    def get_percent_discount(self):
        if self.normal_price and self.discounted_price:
            if self.normal_price > 0:
                discount = ((self.normal_price - self.discounted_price) / self.normal_price) * 100
                return round(discount, 2)
        return Decimal('0.00')
    
    def update_stock(self, quantity_sold):
        self.available_stock -= quantity_sold
        self.sold_count += quantity_sold
        self.last_sold_date = timezone.now()
        self.total_revenue += self.discounted_price * quantity_sold
        self.is_low_stock = self.available_stock <= self.low_stock_threshold
        self.save()
    
    def display_product_image(self):
        return mark_safe('<img src="%s" width= "50" height= "50"/>' %(self.product_image.url))

    def __str__(self):
        return self.product_title


class ProductImages(models.Model):
    additional_images = models.ImageField(upload_to=user_directory_path, default="product.jpg")
    date_added = models.DateTimeField(default=timezone.now)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def display_additional_images(self):
            return mark_safe('<img src="%s" width= "50" height= "50"/>' %(self.additional_images.url))
        
    def __str__(self):
            return f"{self.product.product_title} additional images"

    class Meta:
        verbose_name_plural = "Product images"



class ProductVariation(models.Model):
    vid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="var", alphabet="abcdefghijklmnopqrstuvwxyz1234567890")
    product = models.ForeignKey(Product, related_name='variations', on_delete=models.CASCADE)
    size = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    material = models.CharField(max_length=50, blank=True, null=True)
    weight = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)])
    price_adjustment = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    is_active = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.product_title} - {self.get_variation_name()}"

    def get_variation_name(self):
        attributes = []
        if self.size:
            attributes.append(f"Size: {self.size}")
        if self.color:
            attributes.append(f"Color: {self.color}")
        if self.material:
            attributes.append(f"Material: {self.material}")
        return ", ".join(attributes) if attributes else "Default"

    def get_final_price(self):
        return self.product.discounted_price + self.price_adjustment

    class Meta:
        unique_together = ('product', 'size', 'color', 'material')
        verbose_name = "Product variation"
        verbose_name_plural = "Product variations"


class Cart(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="crt", alphabet="abcdefghijklmnopqrstuvwxyz1234567890")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, validators=[MinValueValidator(0)])

    class Meta:
        verbose_name_plural = "Carts"

    def __str__(self):
        return f"Cart of {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation = models.ForeignKey(ProductVariation, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(0)])
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Cart items"

    def __str__(self):
        return f"{self.product.product_title} in {self.cart.user.username}'s cart"


class Coupon(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="cpn", alphabet="abcdefghijklmnopqrstuvwxyz1234567890")
    code = models.CharField(max_length=50, unique=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
    is_percentage = models.BooleanField(default=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Coupons"

    def __str__(self):
        return self.code


class Shipping(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    estimated_days = models.IntegerField(validators=[MinValueValidator(0)])

    class Meta:
        verbose_name_plural = "Shipping options"

    def __str__(self):
        return self.name


class Order(models.Model):
    ORDER_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('returned', 'Returned'),
    )

    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = ShortUUIDField(unique=True, length=10, max_length=20, prefix="ord", alphabet="abcdefghijklmnopqrstuvwxyz1234567890")
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    address = models.ForeignKey('Address', on_delete=models.SET_NULL, null=True)
    shipping_method = models.ForeignKey('Shipping', on_delete=models.SET_NULL, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    order_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    estimated_delivery_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"Order {self.order_id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product_title = models.CharField(max_length=255)
    order_item_image = models.CharField(max_length=255, default="order item.jpg")
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    class Meta:
        verbose_name_plural = "Order items"
    
    def order_item_img(self):
        return mark_safe('<img src="media/%s" width= "50" height= "50"/>' %(self.order_item_image))

    def __str__(self):
        return f"{self.product_title} ({self.quantity})"


class Wishlist(models.Model):
    wid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="wsh", alphabet="abcdefghijklmnopqrstuvwxyz1234567890")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Wishlists"

    def __str__(self):
        return f"{self.product.product_title} in {self.user.username}'s wishlist"


class Address(models.Model):
    aid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="adr", alphabet="abcdefghijklmnopqrstuvwxyz1234567890")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=20)
    is_default = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Addresses"

    def __str__(self):
        return f"{self.address_line1}, {self.city}, {self.state}, {self.country}, {self.zipcode}"


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
    )
    pid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="pay", alphabet="abcdefghijklmnopqrstuvwxyz1234567890")
    order = models.ForeignKey(Order, related_name='payments', on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    transaction_id = models.CharField(max_length=100, unique=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    payment_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Payments"

    def __str__(self):
        return f"Payment for {self.order.order_id}"


class ProductReview(models.Model):
    rid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="prv", alphabet="abcdefghijklmnopqrstuvwxyz1234567890")
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='product_reviews', on_delete=models.CASCADE)
    review_text = HTMLField(max_length=3067)
    rating = models.IntegerField(choices=RATING, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Product reviews"
        unique_together = ('product', 'user')

    def __str__(self):
        return f"Review by {self.user.username} for {self.product.product_title}"


class VendorReview(models.Model):
    rid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="vrv", alphabet="abcdefghijklmnopqrstuvwxyz1234567890")
    vendor = models.ForeignKey(Vendor, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='vendor_reviews', on_delete=models.CASCADE)
    review_text = HTMLField(max_length=3067)
    rating = models.IntegerField(choices=RATING, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Vendor reviews"
        unique_together = ('vendor', 'user')

    def __str__(self):
        return f"Review by {self.user.username} for {self.vendor.vendor_title}"


class InventoryChange(models.Model):
    icid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="inv", alphabet="abcdefghijklmnopqrstuvwxyz1234567890")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inventory_changes')
    change_amount = models.IntegerField()
    reason = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Inventory changes"

    def __str__(self):
        return f"{self.product.product_title} - {self.change_amount} - {self.timestamp}"


class ProductReturn(models.Model):
    RETURN_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    )

    rid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="ret", alphabet="abcdefghijklmnopqrstuvwxyz1234567890")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='returns')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    reason = HTMLField()
    status = models.CharField(max_length=20, choices=RETURN_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Returned products"

    def __str__(self):
        return f"Return {self.rid} for Order {self.order.order_id}"


class Refund(models.Model):
    REFUND_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    )

    rfid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="ref", alphabet="abcdefghijklmnopqrstuvwxyz1234567890")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='refunds')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = HTMLField()
    status = models.CharField(max_length=20, choices=REFUND_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Refunds"

    def __str__(self):
        return f"Refund {self.rfid} for Order {self.order.order_id}"


class ProductBundle(models.Model):
    bid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="bnd", alphabet="abcdefghijklmnopqrstuvwxyz1234567890")
    name = models.CharField(max_length=255, unique=True)
    description = HTMLField()
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Product bundles"

    def __str__(self):
        return self.name


class BundleItem(models.Model):
    bundle = models.ForeignKey(ProductBundle, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name_plural = "bundle items"

    def __str__(self):
        return f"{self.product.product_title} in {self.bundle.name}"


class Banner(models.Model):
    bid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="ban", alphabet="abcdefghijklmnopqrstuvwxyz1234567890")
    banner_title = models.CharField(max_length=255)
    banner_image = models.ImageField(upload_to='banner', default='default_banner.jpg')
    banner_link = models.URLField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.banner_title

    def display_banner_image(self):
        return mark_safe('<img src="%s" width= "100" height= "50"/>' % (self.banner_image.url))
