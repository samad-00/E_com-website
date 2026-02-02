from django.contrib.auth.models import AnonymousUser
from store.models import CartItem


def cart_context(request):
    """
    Context processor to provide cart information to all templates.
    Handles both session-based cart (anonymous) and database cart (authenticated).
    """
    cart_count = 0
    cart_total = 0
    cart_items = []
    
    if request.user.is_authenticated:
        # Get cart items from database for authenticated users
        cart_items = CartItem.objects.filter(user=request.user)
        cart_count = sum([item.quantity for item in cart_items])
        cart_total = sum([item.get_subtotal() for item in cart_items])
    else:
        # Get cart from session for anonymous users
        cart = request.session.get('cart', {})
        cart_count = len(cart)
    
    return {
        'cart_count': cart_count,
        'cart_total': cart_total,
        'cart_items': cart_items,
    }
