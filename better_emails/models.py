import datetime
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.utils.importlib import import_module
from .managers import AddressManager, ConfirmationManager
from . import app_settings

class Address(models.Model):
    user = models.ForeignKey(User)
    email = models.EmailField()
    verified = models.BooleanField(default=False)
    primary = models.BooleanField(default=False)

    objects = AddressManager()
    
    class Meta:
        verbose_name = _("email address")
        verbose_name_plural = _("email addresses")
        unique_together = (
            ("user", "email"),
        )

    def __unicode__(self):
        return u"%s (%s)" % (self.email, self.user)


class Confirmation(models.Model):
    email_address = models.OneToOneField(Address)
    confirmation_key = models.CharField(max_length=40)
    created = models.DateTimeField()
    
    objects = ConfirmationManager()
    
    class Meta:
        verbose_name = _("email confirmation")
        verbose_name_plural = _("email confirmations")
    
    def __unicode__(self):
        return u"confirmation for %s" % self.email_address

    def key_expired(self):
        if not app_settings.EMAILS_CONFIRMATION_DAYS:
            return False
        expiration_date = self.created + datetime.timedelta(
            days=app_settings.EMAILS_CONFIRMATION_DAYS)
        return expiration_date <= datetime.datetime.now()
    key_expired.boolean = True


if app_settings.EMAILS_RECEIVERS_MODULE:
    import_module(app_settings.EMAILS_RECEIVERS_MODULE)
