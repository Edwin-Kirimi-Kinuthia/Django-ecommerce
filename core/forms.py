from django import forms
from .models import ProductReview, VendorReview
#Third party
from tinymce.widgets import TinyMCE

RATING = (
    (1, "⭐✰✰✰✰"),
    (2, "⭐⭐✰✰✰"),
    (3, "⭐⭐⭐✰✰"),
    (4, "⭐⭐⭐⭐✰"),
    (5, "⭐⭐⭐⭐⭐"),   
)

class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search products...'}))

class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ['review_text', 'rating']
        widgets = {
            'review_text': TinyMCE(attrs={'rows': 10, 'cols': 80}),
            'rating': forms.Select(choices=RATING),
        }

    def __init__(self, *args, **kwargs):
        super(ProductReviewForm, self).__init__(*args, **kwargs)
        self.fields['review_text'].widget.attrs.update({'class': 'form-control'})
        self.fields['rating'].widget.attrs.update({'class': 'form-control'})

class VendorReviewForm(forms.ModelForm):
    class Meta:
        model = VendorReview
        fields = ['vendor', 'review_text', 'rating']
        widgets = {
            'review_text': TinyMCE(attrs={'rows': 10, 'cols': 80}),
            'rating': forms.Select(choices=RATING),
        }

    def __init__(self, *args, **kwargs):
        super(VendorReviewForm, self).__init__(*args, **kwargs)
        self.fields['vendor'].widget.attrs.update({'class': 'form-control'})
        self.fields['review_text'].widget.attrs.update({'class': 'form-control'})
        self.fields['rating'].widget.attrs.update({'class': 'form-control'})
