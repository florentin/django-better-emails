import sys
from django.views.generic import TemplateView
from .models import Confirmation
from .signals import confirmed

class ConfirmationException(Exception):
    pass

class ConfirmationView(TemplateView):
    def confirmation(self):
        """
        Cases:
        * the key is valid and not expired
        * the key expired
        * the key is invalid
        """
        confirmation_key = self.kwargs['key'].lower()
        
        try:
            confirmation = Confirmation.objects.get(confirmation_key=confirmation_key)
        except Confirmation.DoesNotExist:
            raise ConfirmationException('Invalid key.')
            
        if confirmation.key_expired():
            # TODO:  confirmation.delete()
            raise ConfirmationException('The key has expired.')

        try:
            address = confirmation.email_address
            address.verified = True
            address.save()
            confirmed.send(sender=None, 
                           operation=self.kwargs['operation'], 
                           address=address)
        except:
            raise ConfirmationException('We could not verify the user.')
            # TODO: log errors

        return address

    def get(self, request, *args, **kwargs):
        try:
            address = self.confirmation()
        except ConfirmationException as e:
            kwargs.update(error=e)
        else:
            kwargs.update(address=address)
        
        return super(ConfirmationView, self).get(request, *args, **kwargs)

    def get_template_names(self):
        return ["better/emails/confirmation_%s.html"%self.kwargs['operation']]


confirmation = ConfirmationView.as_view()
