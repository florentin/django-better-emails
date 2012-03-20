import sys, datetime
from random import random

from django.conf import settings
from django.db import models
from django.core.mail import send_mail
from django.core.urlresolvers import reverse, NoReverseMatch
from django.template.loader import render_to_string
from django.utils.hashcompat import sha_constructor
from django.utils.translation import gettext_lazy as _
from django.contrib.sites.models import Site
from .signals import confirmed, confirmation_sent

class AddressManager(models.Manager):
    def set_primary(self, email_address):
        if email_address.primary:
            return True
        
        self.get_query_set().filter(user=email_address.user, primary=True).update(primary=False)
        email_address.primary = True
        email_address.save()
        
        if email_address.user.email != email_address.email:
            email_address.user.email = email_address.email
            email_address.user.save()
    
    def get_primary(self, user):
        try:
            return self.get(user=user, primary=True)
        except self.model.DoesNotExist:
            return None
    
    def activate_user(self, email_address):
        email_address.user.is_active = True
        return email_address.user.save()
    
    def get_users_for(self, email):
        """
        returns a list of users with the given email.
        """
        # this is a list rather than a generator because we probably want to
        # do a len() on it right away
        return [address.user for address in \
                self.filter(verified=True, email=email)]


class ConfirmationManager(models.Manager):
    def ask_confirmation(self, email_address, operation):
        salt = sha_constructor(str(random())).hexdigest()[:5]
        confirmation_key = sha_constructor(salt + email_address.email).hexdigest()
        confirmation, created = self.get_or_create(
            email_address=email_address,
            defaults={'created': datetime.datetime.now(),
                      'confirmation_key': confirmation_key
                      }
        )
        
        current_site = Site.objects.get_current()
        # check for the url with the dotted view path
        try:
            path = reverse("better_emails.views.confirmation",
                           args=[operation, confirmation.confirmation_key])
        except NoReverseMatch:
            # or get path with named urlconf instead
            path = reverse("confirmation", args=[operation, confirmation.confirmation_key])
        
        

        protocol = getattr(settings, "DEFAULT_HTTP_PROTOCOL", "http")
        activate_url = u"%s://%s%s" % (
            protocol,
            unicode(current_site.domain),
            path
        )
        context = {
            "user": email_address.user,
            "activate_url": activate_url,
            "current_site": current_site,
            "confirmation_key": confirmation.confirmation_key,
        }
        subject = render_to_string(
            "better/emails/%s_subject.txt"%operation, context)
        # remove superfluous line breaks
        subject = "".join(subject.splitlines())
        message = render_to_string(
            "better/emails/%s_message.txt"%operation, context)
        
        
        if send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email_address.email]):
            confirmation_sent.send(
                sender=self.model,
                operation=operation,
                confirmation=confirmation,
            )
        else:
            # TODO: log the error, warn the admin
            send_mail('Error', "Cannot send confirmation email", settings.DEFAULT_FROM_EMAIL, [settings.DEFAULT_FROM_EMAIL])
            confirmation.delete()
            
        return confirmation
    
    def delete_expired_confirmations(self):
        for confirmation in self.all():
            if confirmation.key_expired():
                confirmation.delete()