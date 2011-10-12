from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from newsletters.models import Subscription
    
class Command(BaseCommand):
    help = "Batch unsubscribe users based on email"
    def handle(self, *args, **opts):
        emailfile, slug = args
        newsletter = Newsletter.objects.get(slug=slug)
        for email in open(emailfile).readlines():
            Subscription.objects.filter(email=email).delete()
