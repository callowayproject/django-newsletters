from django.dispatch import Signal

subscription = Signal(providing_args=['email', 'newsletter'])
unsubscription = Signal(providing_args=['email', 'newsletter'])