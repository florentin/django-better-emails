from django.dispatch import Signal

confirmed = Signal(providing_args=["operation", "address"])
confirmation_sent = Signal(providing_args=["operation", "confirmation"])
