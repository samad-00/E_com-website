from django.urls import path
from . import views

urlpatterns = [
    # Home and Shop
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('search/', views.search, name='search'),
    path('category/<slug:slug>/', views.category_view, name='category'),
    
    # Product
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    
    # Cart
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    # Checkout & Orders
    path('checkout/', views.checkout, name='checkout'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('orders/', views.user_orders, name='user_orders'),
    
    # Wishlist
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/toggle/<int:product_id>/', views.toggle_wishlist, name='toggle_wishlist'),
    
    # Contact & Queries
    path('contact/', views.contact_query, name='contact'),
    path('contact/thank-you/', views.contact_thank_you, name='contact_thank_you'),
]
