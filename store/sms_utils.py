from django.conf import settings

def send_sms(to_number, body):
    """Send SMS via Twilio if credentials provided. Returns True if sent."""
    sid = getattr(settings, 'TWILIO_ACCOUNT_SID', '')
    token = getattr(settings, 'TWILIO_AUTH_TOKEN', '')
    from_number = getattr(settings, 'TWILIO_FROM_NUMBER', '')

    if not (sid and token and from_number and to_number):
        return False

    try:
        from twilio.rest import Client
        client = Client(sid, token)
        client.messages.create(body=body, from_=from_number, to=to_number)
        return True
    except Exception:
        return False
