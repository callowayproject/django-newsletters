from django import forms
from newsletters.models import Subscription, Newsletter

def get_newsletters_with_subs(email):
    """
    Return a list of newsletter dictionaries with the additional key "is_subscribed"
    """
    newsletters = Newsletter.objects.values()
    subs = Subscription.objects.filter(email=email).values_list('newsletter__id', flat=True)
    for item in newsletters:
        item['is_subscribed'] = item['id'] in subs
    return newsletters


class NewsletterForm(forms.Form):
    """
    Create a form with a dynamic choice of newsletter choices.
    
    Subscribed newsletters are checked if there is an email key in the initial
    data.
    """
    email = forms.EmailField()
    
    def __init__(self, *args, **kwargs):
        subscriptions = []
        if 'initial' in kwargs and kwargs['initial'].has_key('email'):
            subscriptions = Subscription.objects.filter(
                email=kwargs['initial']['email']).values_list(
                    'newsletter__name', 'newsletter__id')
        self._subscriptions = dict(subscriptions)
        self._all_newsletters = Newsletter.objects.all()
        for nl in self._all_newsletters:
            self.base_fields[nl.name] = forms.BooleanField(
                label=nl.name,
                initial=nl.id in self._subscriptions.values(),
                required=False,
                widget=forms.widgets.CheckboxInput())
        super(NewsletterForm, self).__init__(*args, **kwargs)
    
    def get_unsubscribes(self):
        """
        Return a list of newsletter objects
        """
        new_subs = self.get_subscriptions()
        unsubscribes = []
        for item in self._subscriptions:
            if item[0] not in new_subs:
                unsubscribes.extend(item[1])
        return Subscription.objects.filter(newsletter__id__in=unsubscribes)
        
    def get_subscriptions(self):
        """
        Shortcut to get the newsletters subscribed in the form
        """
        newsletters = [field for field, val in self.cleaned_data.items() if val and field != 'email']
        return newsletters
            