from django import template
from django.conf import settings
from decimal import Decimal

register = template.Library()


@register.filter
def multiply(value, arg):
    """Multiply the value by the argument."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def divide(value, arg):
    """Divide the value by the argument."""
    try:
        return float(value) / float(arg) if float(arg) != 0 else 0
    except (ValueError, TypeError):
        return 0


@register.filter
def image_url(image_field):
    """Return proper image URL for both local files and external URLs."""
    if not image_field:
        return ''
    
    image_name = str(image_field)
    
    # Check if it's an external URL
    if image_name.startswith('http://') or image_name.startswith('https://'):
        return image_name
    
    # Return local file URL
    return image_field.url if hasattr(image_field, 'url') else image_name

