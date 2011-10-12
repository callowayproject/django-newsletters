from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from django.views.generic.simple import redirect_to


admin.autodiscover()

urlpatterns = patterns('',
    (r'^newsletters/', include('newsletters.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^$', redirect_to, {'url': '/newsletters/'}),
)

if settings.DEBUG:
    urlpatterns = urlpatterns + patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
        )

