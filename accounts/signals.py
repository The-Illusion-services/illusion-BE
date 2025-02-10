# signals.py
from django.core.mail import send_mail
from django.conf import settings
from axes.signals import user_locked_out
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(user_locked_out)
def send_lockout_email(sender, request, **kwargs):
    # Get the user from the request object
    user = request.user if request.user.is_authenticated else None
    
    # If the user is not found, you might want to handle this case
    if user is None:
        return

    # Email content
    subject = 'Account Locked Due to Multiple Failed Login Attempts'
    message = f"User {user.username} has been locked out due to multiple failed login attempts."
    recipient_list = settings.AXES_FAILURE_EMAIL_RECIPIENTS

    # Send the email
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
