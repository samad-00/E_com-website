from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Avg
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
import json
import random
import string

from .models import (
    Category, Product, Review, CartItem, 
    Order, OrderItem, Wishlist, UserProfile, ContactQuery
)
from .forms import ReviewForm, CheckoutForm, ContactQueryForm


# ===========================
# HOME VIEW
# ===========================
def home(request):
    """Home page with featured products and new arrivals."""
    featured_products = Product.objects.filter(is_featured=True)[:8]
    new_products = Product.objects.filter(is_new=True).order_by('-created_at')[:8]
    categories = Category.objects.all()[:5]
    
    context = {
        'featured_products': featured_products,
        'new_products': new_products,
        'categories': categories,
        'page_title': 'Home - Luxury Jewelry Store',
    }
    return render(request, 'store/home.html', context)


# ===========================
# SHOP/PRODUCTS LIST VIEW
# ===========================
def shop(request):
    """Products listing with filters and sorting."""
    products = Product.objects.all()
    categories = Category.objects.all()
    
    # Filter by category
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # Filter by price range
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    if price_min:
        products = products.filter(price__gte=float(price_min))
    if price_max:
        products = products.filter(price__lte=float(price_max))
    
    # Search
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Sorting
    sort_by = request.GET.get('sort', '-created_at')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'rating':
        products = products.annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    else:
        products = products.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    products_page = paginator.get_page(page_number)
    
    context = {
        'products': products_page,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_slug,
        'selected_sort': sort_by,
        'page_title': 'Shop - Jewelry Store',
    }
    return render(request, 'store/shop.html', context)


# ===========================
# PRODUCT DETAIL VIEW
# ===========================
def product_detail(request, slug):
    """Product detail page with reviews and related products."""
    product = get_object_or_404(Product, slug=slug)
    reviews = product.reviews.all()
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    
    # Related products from same category
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id)[:4]
    
    # Check if user has wishlist item
    in_wishlist = False
    if request.user.is_authenticated:
        try:
            in_wishlist = product in request.user.wishlist.products.all()
        except:
            in_wishlist = False
    
    review_form = ReviewForm()
    
    # Handle review submission
    if request.method == 'POST' and request.user.is_authenticated:
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('product_detail', slug=slug)
    
    context = {
        'product': product,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'related_products': related_products,
        'review_form': review_form,
        'in_wishlist': in_wishlist,
        'page_title': f'{product.name} - Jewelry Store',
    }
    return render(request, 'store/product_detail.html', context)


# ===========================
# ADD TO CART
# ===========================
@login_required(login_url='login')
def add_to_cart(request, product_id):
    """Add product to cart."""
    product = get_object_or_404(Product, id=product_id)
    
    try:
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            quantity = 1
        if quantity > product.stock:
            quantity = product.stock
    except (ValueError, TypeError):
        quantity = 1
    
    # Get or create cart item
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': quantity}
    )
    
    if not created:
        cart_item.quantity += quantity
        if cart_item.quantity > product.stock:
            cart_item.quantity = product.stock
        cart_item.save()
    
    messages.success(request, f'{product.name} added to cart!')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f'{product.name} added to cart',
            'cart_count': sum([item.quantity for item in CartItem.objects.filter(user=request.user)])
        })
    
    return redirect('cart')


# ===========================
# VIEW CART
# ===========================
def cart(request):
    """View shopping cart."""
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        cart_items = []
    
    cart_total = sum([item.get_subtotal() for item in cart_items], Decimal(0))
    tax_amount = cart_total * Decimal('0.1')  # 10% tax
    
    context = {
        'cart_items': cart_items,
        'subtotal': cart_total,
        'tax_amount': tax_amount,
        'cart_total': cart_total + tax_amount,
        'page_title': 'Shopping Cart',
    }
    return render(request, 'store/cart.html', context)


# ===========================
# UPDATE CART ITEM
# ===========================
@login_required(login_url='login')
def update_cart(request, item_id):
    """Update cart item quantity."""
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'subtotal': float(cart_item.get_subtotal()),
            'cart_total': float(sum([item.get_subtotal() for item in CartItem.objects.filter(user=request.user)]))
        })
    
    return redirect('cart')


# ===========================
# REMOVE FROM CART
# ===========================
@login_required(login_url='login')
def remove_from_cart(request, item_id):
    """Remove item from cart."""
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_total': float(sum([item.get_subtotal() for item in CartItem.objects.filter(user=request.user)]))
        })
    
    return redirect('cart')


# ===========================
# CHECKOUT VIEW
# ===========================
@login_required(login_url='login')
def checkout(request):
    """Checkout page."""
    cart_items = CartItem.objects.filter(user=request.user)
    
    if not cart_items.exists():
        return redirect('shop')
    
    cart_total = sum([item.get_subtotal() for item in cart_items], Decimal(0))
    tax_amount = cart_total * Decimal('0.08')  # 8% tax
    final_total = cart_total + tax_amount
    form = CheckoutForm()
    
    # Pre-fill form with user profile data
    if request.user.profile:
        form.initial = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'phone': request.user.profile.phone,
            'address': request.user.profile.address,
            'city': request.user.profile.city,
            'state': request.user.profile.state,
            'postal_code': request.user.profile.postal_code,
            'country': request.user.profile.country,
        }
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Create order
            order = form.save(commit=False)
            order.user = request.user
            order.order_number = generate_order_number()
            order.total_price = cart_total
            order.save()
            
            # Create order items
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
            
            # Clear cart
            cart_items.delete()
            
            return redirect('order_confirmation', order_id=order.id)
    
    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'tax_amount': tax_amount,
        'final_total': final_total,
        'form': form,
        'page_title': 'Checkout',
    }
    return render(request, 'store/checkout.html', context)


# ===========================
# ORDER CONFIRMATION
# ===========================
def order_confirmation(request, order_id):
    """Order confirmation page."""
    order = get_object_or_404(Order, id=order_id)

    # Check if user has permission to view this order
    if order.user != request.user and not request.user.is_staff:
        return redirect('home')

    # Calculate tax (8% of total price)
    tax_amount = order.total_price * Decimal('0.08')

    context = {
        'order': order,
        'tax_amount': tax_amount,
        'page_title': f'Order Confirmation - {order.order_number}',
    }
    return render(request, 'store/order_confirmation.html', context)


# ===========================
# USER ORDERS
# ===========================
@login_required(login_url='login')
def user_orders(request):
    """View user's orders."""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    orders_page = paginator.get_page(page_number)
    
    context = {
        'orders': orders_page,
        'page_title': 'My Orders',
    }
    return render(request, 'store/user_orders.html', context)


# ===========================
# WISHLIST FUNCTIONS
# ===========================
@login_required(login_url='login')
def toggle_wishlist(request, product_id):
    """Add/remove product from wishlist."""
    product = get_object_or_404(Product, id=product_id)
    
    try:
        wishlist = request.user.wishlist
    except Wishlist.DoesNotExist:
        wishlist = Wishlist.objects.create(user=request.user)
    
    if product in wishlist.products.all():
        wishlist.products.remove(product)
        in_wishlist = False
    else:
        wishlist.products.add(product)
        in_wishlist = True
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'in_wishlist': in_wishlist,
            'message': 'Added to wishlist' if in_wishlist else 'Removed from wishlist'
        })
    
    return redirect('product_detail', slug=product.slug)


@login_required(login_url='login')
def wishlist_view(request):
    """View user's wishlist."""
    try:
        wishlist_items = request.user.wishlist.products.all()
    except Wishlist.DoesNotExist:
        wishlist_items = []
    
    context = {
        'wishlist_items': wishlist_items,
        'page_title': 'My Wishlist',
    }
    return render(request, 'store/wishlist.html', context)


# ===========================
# HELPER FUNCTIONS
# ===========================
def generate_order_number():
    """Generate unique order number."""
    date_str = timezone.now().strftime('%Y%m%d')
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f'ORD-{date_str}-{random_str}'


# ===========================
# CATEGORY VIEW
# ===========================
def category_view(request, slug):
    """View products in a category."""
    category = get_object_or_404(Category, slug=slug)
    products = category.products.all()
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    products_page = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'products': products_page,
        'page_title': f'{category.name} - Jewelry Store',
    }
    return render(request, 'store/category.html', context)


# ===========================
# SEARCH VIEW
# ===========================
def search(request):
    """Search products."""
    query = request.GET.get('q', '')
    products = []
    
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )
    
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    products_page = paginator.get_page(page_number)
    
    context = {
        'query': query,
        'products': products_page,
        'page_title': f'Search Results - {query}',
    }
    return render(request, 'store/search.html', context)


# ===========================
# CONTACT QUERY VIEW
# ===========================
def contact_query(request):
    """Handle customer contact inquiries and product queries."""
    if request.method == 'POST':
        form = ContactQueryForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            # If user is authenticated, link to their email
            if request.user.is_authenticated:
                contact.email = request.user.email
            contact.save()
            messages.success(request, 'Thank you! Your query has been submitted. We will respond shortly.')
            return redirect('contact_thank_you')
    else:
        form = ContactQueryForm()
        # Pre-fill email if user is authenticated
        if request.user.is_authenticated:
            form.initial['email'] = request.user.email
            form.initial['name'] = request.user.get_full_name() or request.user.username
    
    context = {
        'form': form,
        'page_title': 'Contact Us - KIRAA',
    }
    return render(request, 'store/contact.html', context)


def contact_thank_you(request):
    """Thank you page after contact form submission."""
    return render(request, 'store/contact_thank_you.html', {
        'page_title': 'Thank You - KIRAA',
    })
