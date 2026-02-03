from django import forms
from store.models import Review, Order, ContactQuery


# ===========================
# REVIEW FORM
# ===========================
class ReviewForm(forms.ModelForm):
    """Form for product reviews."""
    RATING_CHOICES = (
        (5, '⭐⭐⭐⭐⭐ Excellent'),
        (4, '⭐⭐⭐⭐ Good'),
        (3, '⭐⭐⭐ Average'),
        (2, '⭐⭐ Poor'),
        (1, '⭐ Very Poor'),
    )
    
    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input'
        })
    )
    
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Share your thoughts about this product',
                'rows': 5
            })
        }


# ===========================
# CHECKOUT FORM
# ===========================
class CheckoutForm(forms.ModelForm):
    """Form for checkout and order placement."""
    coupon_code = forms.CharField(required=False, label='Coupon Code', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter coupon code (optional)'}))
    
    class Meta:
        model = Order
        fields = [
            'first_name', 'last_name', 'email', 'phone',
            'address', 'city', 'state', 'postal_code', 'country',
            'payment_method'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Street Address',
                'rows': 3
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City'
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'State/Province'
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Postal Code'
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Country'
            }),
            'payment_method': forms.RadioSelect(attrs={
                'class': 'form-check-input'
            }),
        }

# ===========================
# CONTACT QUERY FORM
# ===========================
class ContactQueryForm(forms.ModelForm):
    """Form for customer contact inquiries and product queries."""
    
    class Meta:
        model = ContactQuery
        fields = ['name', 'email', 'phone', 'query_type', 'product', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Email',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Phone (Optional)'
            }),
            'query_type': forms.Select(attrs={
                'class': 'form-control form-select',
                'required': True
            }),
            'product': forms.Select(attrs={
                'class': 'form-control form-select'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Query Subject',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe your query or question in detail...',
                'rows': 6,
                'required': True
            }),
        }