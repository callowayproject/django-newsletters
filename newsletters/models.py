from django.db import models
from django.core.files.storage import get_storage_class
from categories.models import Category

from settings import ADVERTISEMENT_STORAGE, POSITIONS

class Newsletter(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    template = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, null=True)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ('name', )
    
    @models.permalink
    def get_absolute_url(self):
        return ('newsletter_detail', (), {'slug': self.slug})


class Subscription(models.Model):
    """
    Subscription to the portal newsletter.
    """
    email = models.EmailField()
    newsletter = models.ForeignKey(Newsletter)
    subscription_date = models.DateTimeField(auto_now_add=True)
    hashkey = models.CharField(max_length=100, blank=True)
    confirmed = models.BooleanField(default=False)

    class Meta:
        ordering = ('email', 'newsletter')
        unique_together = ('email', 'newsletter')

    def __unicode__(self):
        return '%s subscription for %s' % (self.newsletter, self.email)

    def save(self, *args, **kwargs):
        if not self.hashkey:
            self.hashkey = self.make_key()
        super(Subscription, self).save(*args, **kwargs)

    def make_key(self):
        from hashlib import sha1
        import random
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        salt = ''.join([random.choice(chars) for i in xrange(50)])
        return sha1(salt + self.email + self.newsletter.name).hexdigest()


class AdvertisementManager(models.Manager):
    def active(self):
        """
        Active ads
        """
        return self.get_query_set(active=True)
    
    def current_set(self, newsletter=None):
        """
        Return the current ads for the given newsletter
        """
        if newsletter is None:
            newsletters = models.Q(newsletter=newsletter)
        else:
            newsletters = (models.Q(newsletter=newsletter) | 
                           models.Q(newsletter=None))
        
        qset = self.active()
        results = qset.filter(newsletters).order_by('position', 'newsletter')
        
        items = dict([(x, None) for x, y in POSITIONS])
        
        for item in results:
            if items[item.position] is None:
                items[item.position] = item
        return items


class Advertisement(models.Model):
    """
    An advertisement for a newsletter
    """
    link = models.URLField(verify_exists=False)
    image = models.FileField(
        upload_to='newsletters/ads/',
        storage=get_storage_class(ADVERTISEMENT_STORAGE)())
    position = models.IntegerField(choices=POSITIONS)
    active = models.BooleanField(default=True)
    newsletter = models.ForeignKey(Newsletter, blank=True, null=True)
    objects = AdvertisementManager()
    
    def thumb(self):
        return '<img src="%s" />' % self.image.url
    thumb.allow_tags = True
    thumb.short_description = 'Thumbnail'
    
    @models.permalink
    def get_absolute_url(self):
        if self.newsletter:
            return ('newsletter_detail', (), {'slug': self.newsletter.slug})
        return ('newsletter_list', (), {})

    def __unicode__(self):
        return self.get_position_display()
    
    