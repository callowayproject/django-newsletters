from django.contrib import admin
from newsletters.models import Newsletter, Advertisement, Subscription

class NewsletterAdmin(admin.ModelAdmin):
    prepopulated_fields = {
       "slug": ("name",)
    }

class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('thumb', 'active', 'newsletter', '__unicode__')
    list_filter = ('active', 'newsletter', )

class SubscriptionAdmin(admin.ModelAdmin):
    fields = ('email', 'newsletter', 'confirmed', )
    list_display = ('email', 'newsletter', 'subscription_date')
    list_filter = ('newsletter', )

admin.site.register(Newsletter, NewsletterAdmin)
admin.site.register(Advertisement, AdvertisementAdmin)
admin.site.register(Subscription, SubscriptionAdmin)