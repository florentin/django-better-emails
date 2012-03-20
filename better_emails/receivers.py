from django.dispatch import receiver
from better_auth.signals import signup_complete, email_complete
from .models import Address, Confirmation

@receiver(signup_complete, sender=None)
def signup_complete_handle(sender, user, **kwargs):
    address = Address.objects.create(user=user, email=user.email)
    Address.objects.set_primary(address)
    Confirmation.objects.ask_confirmation(address, 'signup')


@receiver(email_complete, sender=None)
def email_complete_handle(sender, user, email, **kwargs):
    address, created = Address.objects.get_or_create(user=user, email=email)
    Confirmation.objects.ask_confirmation(address, 'email')
