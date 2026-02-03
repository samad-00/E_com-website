from django.urls import path
from . import views
from . import chat_views

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
    path('order-cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('orders/', views.user_orders, name='user_orders'),
    # Analytics Dashboard
    path('dashboard/', views.analytics_dashboard, name='analytics'),
    
    # Wishlist
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/toggle/<int:product_id>/', views.toggle_wishlist, name='toggle_wishlist'),
    
    # Contact & Queries
    path('contact/', views.contact_query, name='contact'),
    path('contact/thank-you/', views.contact_thank_you, name='contact_thank_you'),
    
    # AI Chat API
    path('api/chat/', chat_views.chat_api, name='chat_api'),
    path('api/products/', chat_views.product_search_api, name='product_search_api'),
]
