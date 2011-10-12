from django.core.management.commands import BaseCommand
from core import pidfile
from newsletters import maintenance

NEWSLETTER_PID_FILE = 'newsletter.pid'

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        pidfile.acquire(NEWSLETTER_PID_FILE) or exit(1)
        maintenance.instance.main()
        pidfile.release(NEWSLETTER_PID_FILE)