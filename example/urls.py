from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from django.views.generic.simple import redirect_to, direct_to_template


admin.autodiscover()

urlpatterns = patterns('',
    (r'^newsletters/', include('newsletters.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^test_ajax', direct_to_template, {'template': 'test_ajax.html'}),
    (r'^$', redirect_to, {'url': '/newsletters/'}),
)

if settings.DEBUG:
    urlpatterns = urlpatterns + patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
        )


from newsletters.signals import subscription, unsubscription

def print_subscription(sender, email, newsletter, *args, **kwargs):
    print "Subscription Event!"
    print email, newsletter

subscription.connect(print_subscription)

def print_unsubscription(sender, email, newsletter, *args, **kwargs):
    print "Unsubscription Event!"
    print email, newsletter

unsubscription.connect(print_unsubscription)