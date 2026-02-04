
import json
import stripe
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt

from store.models import Order, OrderItem
from store.email_utils import send_order_confirmation_email, send_low_stock_alert
from store.sms_utils import send_sms

stripe.api_key = getattr(settings, 'STRIPE_SECRET_KEY', '')


def create_checkout_session(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # Build line items from order items
    line_items = []
    currency = 'usd'

    for item in order.items.all():
        line_items.append({
            'price_data': {
                'currency': currency,
                'product_data': {'name': item.product.name},
                'unit_amount': int(item.price * 100),
            },
            'quantity': int(item.quantity),
        })

    success_url = request.build_absolute_uri(
        f"/store/order_confirmation/{order.id}/?session_id={{CHECKOUT_SESSION_ID}}"
    )
    cancel_url = request.build_absolute_uri('/cart/')

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
            metadata={'order_id': str(order.id)}
        )
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

    # Mark order payment method and keep pending until webhook confirms
    order.payment_method = 'stripe'
    order.status = 'pending'
    order.save()

    return redirect(session.url)


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')
    endpoint_secret = getattr(settings, 'STRIPE_WEBHOOK_SECRET', '')

    event = None

    try:
        if endpoint_secret:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        else:
            event = json.loads(payload)
    except Exception:
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event and event.get('type') == 'checkout.session.completed':
        data = event['data']['object']
        metadata = data.get('metadata', {})
        order_id = metadata.get('order_id') or data.get('client_reference_id')
        if order_id:
            try:
                order = Order.objects.get(id=int(order_id))
                order.paid = True
                order.transaction_id = data.get('payment_intent') or data.get('id')
                order.status = 'confirmed'
                order.save()

                # Decrement stock for each order item and send low-stock alerts
                threshold = getattr(settings, 'LOW_STOCK_THRESHOLD', 5)
                for item in order.items.all():
                    product = item.product
                    if product:
                        try:
                            product.stock = max(0, int(product.stock) - int(item.quantity))
                            product.save()
                            if product.stock <= int(threshold):
                                admin_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None)
                                send_low_stock_alert(product, product.stock, admin_email=admin_email)
                        except Exception:
                            pass

                # Send order confirmation email after successful payment
                try:
                    send_order_confirmation_email(order)
                except Exception:
                    pass

                # Send SMS notification to customer (if phone available)
                try:
                    if order.phone:
                        msg = f'Your order {order.order_number} has been confirmed. Total: {order.total_price}'
                        send_sms(order.phone, msg)
                except Exception:
                    pass
            except Order.DoesNotExist:
                pass

    return HttpResponse(status=200)
