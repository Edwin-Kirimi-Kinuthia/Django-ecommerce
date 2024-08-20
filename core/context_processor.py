from .models import *
from .forms import SearchForm
from django.db.models import Min, Max

def default(request):
    categories = Category.objects.all()
    vendors = Vendor.objects.all()
    tags = Tags.objects.all()
    search_form = SearchForm()
    
    min_price = Product.objects.aggregate(Min('discounted_price'))['discounted_price__min']
    max_price = Product.objects.aggregate(Max('discounted_price'))['discounted_price__max']

    return {
        "categories": categories,
        "vendors": vendors,
        "tags": tags,
        "search_form": search_form,
        "min_price": min_price,
        "max_price": max_price,
    }