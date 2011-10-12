from django.conf import settings

from django.contrib.site.models import Site

current_site = Site.objects.get_current()

DEFAULT_SETTINGS = {
    'POSITIONS': (
        (1,'Leaderboard'),
        (2,'Medium Rectangle'),
        (3,'Button 1 (1)'),
        (4,'Button 1 (2)'),
    ),
    'DEFAULT_TEMPLATE': 'newsletters/default.html',
    'ADVERTISEMENT_STORAGE': settings.DEFAULT_FILE_STORAGE,
}

USER_SETTINGS = DEFAULT_SETTINGS.copy()

USER_SETTINGS.update(getattr(settings, 'NEWSLETTER_SETTINGS', {}))

globals().update(USER_SETTINGS)