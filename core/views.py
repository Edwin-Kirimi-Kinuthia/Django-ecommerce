import os
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from .models import *
from .forms import VendorReviewForm, ProductReviewForm, SearchForm
from django.db.models import Q
from django.db.models import Avg
from django.http import JsonResponse
from django.conf import settings
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.db.models import Min, Max

# Create your views here.
@csrf_exempt
def upload_image(request):
    if request.method == 'POST':
        image_file = request.FILES.get('file')
        if image_file:
            file_path = os.path.join(settings.MEDIA_ROOT, image_file.name)
            file_name = default_storage.save(file_path, image_file)
            file_url = default_storage.url(file_name)
            return JsonResponse({'location': file_url})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def search_view(request):
    form = SearchForm(request.GET)
    results = []

    if form.is_valid():
        query = form.cleaned_data['query']
        if query:
            results = Product.objects.filter(
                Q(product_title__icontains=query) |
                Q(description__icontains=query) |
                Q(category__category_title__icontains=query) |
                Q(subcategory__subcategory_title__icontains=query) |
                Q(vendor__vendor_title__icontains=query)
            ).distinct()
    
    context = {
        'form': form,
        'results': results,
        'query': query if query else ''
    }
    return render(request, 'core/search-results.html', context)

def index(request):
    products= Product.objects.filter(product_status="published", featured=True, in_stock= True).order_by("updated")
    banners = Banner.objects.filter(is_active=True).order_by("bid")

    context = {
        'products': products,
        'banners': banners,
    }
    return render(request, 'core/index.html', context)

def product_list_view(request):
    products= Product.objects.filter(product_status="published").order_by("-updated")
    return render(request, 'core/product-list.html', {'products': products})

def category_list(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'core/category-list.html', context)

def subcategory_list(request, cid):
    category = get_object_or_404(Category, cid=cid)
    subcategories = category.subcategories.all()
    context = {
        'category': category,
        'subcategories': subcategories
    }
    return render(request, 'core/subcategory-list.html', context)

def product_by_subcategory(request, scid):
    subcategory = get_object_or_404(Subcategory, scid=scid)
    products = Product.objects.filter(subcategory=subcategory, product_status="published", in_stock= True)
    context = {
        'subcategory': subcategory,
        'products': products
    }
    return render(request, 'core/product-by-subcategory.html', context)

def tag_products(request, tag_slug):
    tag = get_object_or_404(Tags, slug=tag_slug)
    products = Product.objects.filter(tags=tag, product_status="published", in_stock=True)
    context = {
        'tag': tag,
        'products': products
    }
    return render(request, 'core/tag_products.html', context)

def vendor_detail(request, vid):
    vendor = get_object_or_404(Vendor, vid=vid)
    reviews = VendorReview.objects.filter(vendor=vendor)
    products = Product.objects.filter(vendor=vendor, product_status="published", in_stock=True)[:8]


    existing_review = None
    if request.user.is_authenticated:
        existing_review = VendorReview.objects.filter(vendor=vendor, user=request.user).first()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect(reverse('userauths:sign-in'))
        
        if existing_review:
            messages.error(request, 'You have already reviewed this vendor!')
            return redirect('core:vendor-detail', vid=vid)

        review_form = VendorReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.vendor = vendor
            review.user = request.user
            review.save()
            return redirect('core:vendor-detail', vid=vid)
    else:
        review_form = VendorReviewForm(initial={'vendor': vendor})

    context = {
        'vendor': vendor,
        'reviews': reviews,
        'review_form': review_form,
        'existing_review': existing_review,
        'products': products,
    }
    return render(request, 'core/vendor-detail.html', context)

def product_detail(request, pid):
    product = get_object_or_404(Product, pid=pid)
    related_products = Product.objects.filter(category=product.category).exclude(pid=pid)[:4]
    tags = product.tags.all()
    reviews = product.reviews.all().order_by('-created_at')
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    
    user_review = None
    if request.user.is_authenticated:
        user_review = ProductReview.objects.filter(user=request.user, product=product).first()

    if request.method == 'POST' and request.user.is_authenticated:
        if not user_review:
            review_form = ProductReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.user = request.user
                review.product = product
                review.save()
                messages.success(request, "Your review has been submitted.")
                return redirect('core:product-detail', pid=pid)
        else:
            messages.error(request, "You have already reviewed this product.")
    else:
        review_form = ProductReviewForm()

    context = {
        'product': product,
        'related_products': related_products,
        'tags': tags,
        'reviews': reviews,
        'average_rating': average_rating,
        'review_form': review_form,
        'user_review': user_review,
    }
    return render(request, 'core/product-detail.html', context)

@login_required
def add_to_cart(request, pid):
    if request.method == 'POST':
        product = get_object_or_404(Product, pid=pid)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
        
        if not item_created:
            cart_item.quantity += 1
            cart_item.save()

        return JsonResponse({'status': 'success', 'message': 'Product added to cart'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@login_required
def add_to_wishlist(request, pid):
    if request.method == 'POST':
        product = get_object_or_404(Product, pid=pid)
        wishlist, created = Wishlist.objects.get_or_create(user=request.user, product=product)
        
        if created:
            return JsonResponse({'status': 'success', 'message': 'Product added to wishlist'})
        else:
            return JsonResponse({'status': 'info', 'message': 'Product already in wishlist'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@login_required
def buy_now(request, pid):

    return redirect('core:checkout', pid=pid)

def filter_products(request):
    categories = request.GET.getlist('category[]')
    vendors = request.GET.getlist('vendor[]')
    price = request.GET.get('price')
   
    products = Product.objects.filter(product_status="published").distinct()
   
    if categories:
        products = products.filter(category__cid__in=categories)

    if vendors:
        products = products.filter(vendor__vid__in=vendors)

    if price:
        products = products.filter(discounted_price__lte=float(price))

    data = render_to_string('core/async/filtered-products.html', {
        "products": products
    })

    return JsonResponse({"data": data})
