from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings


class Command(BaseCommand):
    help = 'Test email configuration by sending a test email'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--to-email',
            type=str,
            required=True,
            help='Email address to send test email to'
        )
    
    def handle(self, *args, **options):
        to_email = options['to_email']
        
        self.stdout.write('Testing email configuration...')
        self.stdout.write(f'Email backend: {settings.EMAIL_BACKEND}')
        self.stdout.write(f'Email host: {settings.EMAIL_HOST}')
        self.stdout.write(f'Email port: {settings.EMAIL_PORT}')
        self.stdout.write(f'Email user: {settings.EMAIL_HOST_USER}')
        self.stdout.write(f'Email TLS: {settings.EMAIL_USE_TLS}')
        self.stdout.write(f'From email: {settings.DEFAULT_FROM_EMAIL}')
        
        try:
            result = send_mail(
                subject='KIRAA Test Email',
                message='This is a test email from KIRAA jewelry store.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[to_email],
                fail_silently=False,
            )
            
            if result:
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Test email sent successfully to {to_email}!')
                )
            else:
                self.stdout.write(
                    self.style.ERROR('❌ Email send failed - result was 0')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Email send failed with error: {str(e)}')
            )