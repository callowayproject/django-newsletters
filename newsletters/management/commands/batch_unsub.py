from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from newsletters.models import Newsletter
    
class Command(BaseCommand):
    help = "Batch unsubscribe users based on email"
    def handle(self, *args, **opts):
        emailfile,slug = args
        newsletter = Newsletter.objects.get(slug=slug)
        for email in open(emailfile).readlines():
            try:
                user = User.objects.get(email=email.strip())
            except User.DoesNotExist:
                continue
            profile = user.get_profile()
            profile.newsletters.delete(newsletter)
            profile.save()