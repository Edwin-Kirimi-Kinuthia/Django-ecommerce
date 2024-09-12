from .models import *
from .forms import SearchForm
from django.db.models import Min, Max, Sum, F

def default(request):
    categories = Category.objects.all()
    vendors = Vendor.objects.all()
    tags = Tags.objects.all()
    search_form = SearchForm()
    
    min_price = Product.objects.aggregate(Min('discounted_price'))['discounted_price__min']
    max_price = Product.objects.aggregate(Max('discounted_price'))['discounted_price__max']

    cart_items = []
    cart_total = 0
    cart_count = 0

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart).annotate(
            total_price=F('quantity') * F('product__discounted_price')
        ).values('product__product_title', 'product__product_image', 'quantity', 'total_price', 'id')

        cart_total = cart_items.aggregate(Sum('total_price'))['total_price__sum'] or 0
        cart_count = cart_items.aggregate(Sum('quantity'))['quantity__sum'] or 0

    return {
        "categories": categories,
        "vendors": vendors,
        "tags": tags,
        "search_form": search_form,
        "min_price": min_price,
        "max_price": max_price,
        "cart_items": list(cart_items),
        "cart_total": float(cart_total),
        "cart_count": cart_count,
    }