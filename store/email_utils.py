from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


def send_html_email(subject, to_email, template_name, context):
    """Render templates (text and html) and send an EmailMultiAlternatives."""
    text_body = render_to_string(f'emails/{template_name}.txt', context)
    html_body = render_to_string(f'emails/{template_name}.html', context)

    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'webmaster@localhost'),
        to=[to_email],
    )
    msg.attach_alternative(html_body, 'text/html')
    msg.send(fail_silently=True)


def send_order_confirmation_email(order):
    subject = f'Order Confirmation - {order.order_number}'
    to_email = order.email
    context = {'order': order}
    send_html_email(subject, to_email, 'order_confirmation', context)


def send_contact_receipt_email(contact):
    subject = f'We received your inquiry: {contact.subject}'
    to_email = contact.email
    context = {'contact': contact}
    send_html_email(subject, to_email, 'contact_receipt', context)


def notify_admin_new_contact(contact, admin_email):
    subject = f'New contact query: {contact.subject}'
    context = {'contact': contact}
    send_html_email(subject, admin_email, 'new_contact_admin', context)


def send_low_stock_alert(product, current_stock, admin_email=None):
    """Notify admin when a product reaches low stock."""
    subject = f'Low stock alert: {product.name}'
    context = {
        'product': product,
        'current_stock': current_stock,
    }
    if not admin_email:
        from django.conf import settings as _settings
        admin_email = getattr(_settings, 'DEFAULT_FROM_EMAIL', None)
    if admin_email:
        send_html_email(subject, admin_email, 'low_stock_alert', context)


def notify_moderator_review(review, admin_email):
    subject = f'New review for moderation: {review.product.name}'
    context = {'review': review}
    send_html_email(subject, admin_email, 'new_review_moderation', context)


def send_order_cancellation_email(order):
    """Send order cancellation confirmation email."""
    subject = f'Order Cancelled - {order.order_number}'
    to_email = order.email
    context = {'order': order}
    send_html_email(subject, to_email, 'order_cancellation', context)
