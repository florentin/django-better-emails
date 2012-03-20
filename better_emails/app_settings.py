from django.conf import settings

EMAILS_CONFIRMATION_DAYS = getattr(settings,
'EMAILS_CONFIRMATION_DAYS', 30)

EMAILS_RECEIVERS_MODULE = getattr(settings,
'EMAILS_RECEIVERS', "better.emails.receivers")

