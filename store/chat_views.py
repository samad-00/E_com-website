"""
AI Chatbot views for handling customer inquiries
"""

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone
from store.models import Product, Category
import json

# Simple rule-based chatbot for jewelry store
JEWELRY_RESPONSES = {
    'hello': 'Hello! Welcome to our luxury jewelry store. How can I help you today? You can ask about our products, prices, shipping, or anything else!',
    'hi': 'Hi there! 👋 Welcome to KIRAA Jewelry. What can I help you with?',
    'product': 'We offer a beautiful collection of jewelry including rings, necklaces, earrings, and bracelets. We also have premium beauty products. What interests you?',
    'ring': 'We have stunning rings including Diamond Solitaire, Sapphire Engagement, and Emerald and Gold rings. Each piece is exquisitely crafted. Would you like details on any?',
    'necklace': 'Our necklace collection features Gold Pearl Pendants, Crystal Charm Necklaces, and Diamond Tennis Necklaces. All pieces are luxury crafted. Interested in any?',
    'earring': 'We offer Diamond Stud Earrings, Pearl Drop Earrings, and Rose Gold Chandelier Earrings. Find your perfect pair!',
    'bracelet': 'Browse our bracelet collection: Diamond Tennis Bracelet, Gold Bangle Bracelet, and Sapphire and Diamond Bracelet.',
    'price': 'Our prices vary based on the piece. You can view all products with prices on our shop page. Would you like a specific recommendation?',
    'shipping': 'We offer fast and secure shipping to most locations. Shipping costs and timelines will be shown during checkout.',
    'payment': 'We accept all major credit cards and process payments securely through Stripe. Your data is fully encrypted.',
    'beauty': 'We also carry luxury beauty products: Premium Lipstick Set, Luxury Face Serum, and Hydrating Face Cream.',
    'order': 'You can place orders directly through our website shop. Add items to cart and proceed to checkout.',
    'contact': 'For detailed inquiries, you can contact us through our contact page. We respond within 24 hours!',
    'help': 'I can help you with: products, prices, shipping, orders, beauty products, or general questions. What would you like to know?',
}

def get_ai_response(user_message):
    """
    Generate AI response based on user message
    Uses keyword matching with fallback to general response
    """
    message_lower = user_message.lower().strip()
    
    # Check for keyword matches
    for keyword, response in JEWELRY_RESPONSES.items():
        if keyword in message_lower:
            return response
    
    # If no keywords match, provide helpful default response
    if any(word in message_lower for word in ['what', 'which', 'how', 'where', 'when']):
        return "That's a great question! I can help with information about our products, pricing, shipping, payments, and more. Feel free to ask me anything specific about our jewelry or beauty products!"
    
    if any(word in message_lower for word in ['thank', 'thanks', 'appreciate', 'great', 'love']):
        return "You're welcome! 😊 Is there anything else I can help you with today?"
    
    # Default response
    return "Thanks for your message! I'm here to help with any questions about our products, orders, shipping, or anything else. What would you like to know?"

@csrf_exempt
@require_POST
def chat_api(request):
    """
    API endpoint for chatbot messages
    Receives user message and returns AI response
    """
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return JsonResponse({
                'success': False,
                'error': 'Message is required'
            }, status=400)
        
        # Get AI response
        response = get_ai_response(user_message)
        
        return JsonResponse({
            'success': True,
            'message': response,
            'timestamp': str(timezone.now())
        })
    
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@csrf_exempt
def product_search_api(request):
    """
    API endpoint to search products
    Used by chatbot to find products based on user queries
    """
    query = request.GET.get('q', '').lower()
    
    if not query:
        return JsonResponse({'products': []})
    
    products = Product.objects.filter(
        name__icontains=query
    ) | Product.objects.filter(
        description__icontains=query
    )[:5]
    
    data = {
        'products': [
            {
                'id': p.id,
                'name': p.name,
                'price': str(p.price),
                'slug': p.slug,
                'category': p.category.name if p.category else 'N/A'
            }
            for p in products
        ]
    }
    
    return JsonResponse(data)
