from django.core.mail import send_mail
from django.contrib.sites.models import Site
from django.shortcuts import render_to_response, get_object_or_404
from django.template import loader, Context, RequestContext
from django.template.loader import select_template
from django.http import (Http404, HttpResponseNotAllowed,
                         HttpResponseRedirect)
from django.core.urlresolvers import reverse

from newsletters.models import Newsletter, Advertisement, Subscription
from newsletters.settings import (DEFAULT_TEMPLATE, AUTO_CONFIRM, FROM_EMAIL, 
                                EMAIL_NOTIFICATION_SUBJECT)
from newsletters.forms import NewsletterForm, get_newsletters_with_subs
from newsletters.jsonresponse import JSONResponse


def is_json_request(request):
    """
    Provide True/False for if the request wants the result in json
    
    with format=json in the request
    """
    return ('format' in request.REQUEST and 
            request.REQUEST['format'].lower() == 'json')
    
def sync_subscriptions(sub_form):
    """
    Do all the work of (un)subscribing newsletters for an account
    """
    old_subs = Subscription.objects.filter(email=sub_form.cleaned_data['email'])
    old_subs_nl = [item.newsletter for item in old_subs]
    new_subs = Newsletter.objects.filter(name__in=sub_form.get_subscriptions())
    
    unsubs = [sub for sub in old_subs if sub.newsletter not in new_subs]
    unsub_nl = [sub.newsletter for sub in unsubs]
    subs = [nl for nl in new_subs if nl not in old_subs_nl]
    
    for item in unsubs:
        item.delete()
    for item in subs:
        sub = Subscription.objects.create(
            email=sub_form.cleaned_data['email'],
            newsletter=item,
            confirmed=AUTO_CONFIRM,
        )
    send_notification(unsub_nl, subs, sub_form.cleaned_data['email'])
    return unsub_nl, subs

def send_notification(unsub_newsletters, sub_newsletters, email):
    """
    Send an email notifying the ``email`` recipient they have been
    subscribed to the newsletters in sub_newsletters, and/or unsubscribed
    from the newsletters in unsub_newsletters.
    """
    current_site = Site.objects.get_current()
    
    t = loader.get_template('newsletters/notification_email.txt')
    c = Context({
        'unsubscriptions': unsub_newsletters, 
        'subscriptions': sub_newsletters,
        'site': current_site,
        'email': email,
    })
    send_mail(EMAIL_NOTIFICATION_SUBJECT, t.render(c), FROM_EMAIL, [email], 
            fail_silently=False)


def detail(request, newsletter_slug):
    """
    Provide a rendered HTML version of the newsletter
    """
    newsletter = get_object_or_404(Newsletter, slug=newsletter_slug)
    
    templates = [
        'newsletters/%s.html' % newsletter_slug,
        'newsletters/%s.html' % newsletter.category.slug,
        DEFAULT_TEMPLATE
    ]
    if newsletter.template:
        templates.insert(newsletter.template, 0)
    
    return render_to_response(select_template(templates), {
        'newsletter': newsletter,
        'category': newsletter.category,
        'ads': Advertisement.objects.current_set(newsletter)
    }, RequestContext(request))

def manage(request, email=None):
    """
    Provide a way to manage all subscriptions for a user
    """
    message = []
    if request.method == 'GET' and email:
        if is_json_request(request):
            return JSONResponse({
                'newsletters': get_newsletters_with_subs(email)})
        form = NewsletterForm(initial={'email': email})
    elif request.method == 'GET' and email is None:
        return HttpResponseRedirect(
            reverse('newsletters_list'))
    elif request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            unsubs, subs = sync_subscriptions(form)
            if unsubs:
                message.append(
                    "Successfully unsubscribed from %s" % 
                    ', '.join(map(unicode, unsubs)))
            if subs:
                message.append(
                    "Successfully subscribed to %s" % 
                    ', '.join(map(unicode,subs)))
        if is_json_request(request):
            return JSONResponse({
                'newsletters': get_newsletters_with_subs(email),
                'messages': message})
    return render_to_response('newsletters/manage.html', {
        'newsletters': Newsletter.objects.all(),
        'form': form,
        'messages': message
    }, RequestContext(request))


def newsletter_list(request):
    """
    Return a list of newsletters
    """
    if request.method == 'GET' and 'u' in request.GET:
        return HttpResponseRedirect(
            reverse('newsletters_manage', kwargs={'email': request.GET['u']}))
    if is_json_request(request):
        if 'category__id' in request.REQUEST:
            cat = request.REQUEST['category__id']
            newsletters = Newsletter.objects.filter(category__id=cat).values()
        elif 'category__slug' in request.REQUEST:
            cat = request.REQUEST['category__slug']
            newsletters = Newsletter.objects.filter(category__slug=cat).values()
        else:
            newsletters = Newsletter.objects.values()
        return JSONResponse(
            {'newsletters': newsletters, 
            'signup_url': reverse('newsletters_bulk_subscribe')})
    return render_to_response('newsletters/list.html', {
        'newsletters': Newsletter.objects.all(),
        'form': NewsletterForm(),
    }, RequestContext(request))


def is_subscribed(request, newsletter_slug):
    """
    Is the user subscribed to the newsletter. Requires GET params of
    email
    """
    if 'email' in request.REQUEST and 'id' in request.REQUEST:
        try:
            Subscription.objects.get(
                email=request.REQUEST['email'], 
                newsletter__slug=newsletter_slug)
            return JSONResponse({'is_subscribed': True})
        except Subscription.ObjectDoesNotExist:
            return JSONResponse({'is_subscribed': False})


def subscribe(request, newsletter_slug):
    """
    Subscribe a user to the newsletter
    
    Requires a POST with an email
    """
    newsletter = get_object_or_404(Newsletter, slug=newsletter_slug)
    if request.method != 'POST':
        if is_json_request:
            return JSONResponse({
                'success': False, 
                'message': 'Only POST methods are allowed.'})
        return HttpResponseNotAllowed(['POST',])
    if 'email' not in request.POST:
        if is_json_request:
            return JSONResponse({
                'success': False, 
                'message': 'No email field was included.'})
        raise Http404("email not included in POST")
    try:
        sub = Subscription.objects.get(email=request.POST['email'],
                                       newsletter=newsletter)
    except Subscription.DoesNotExist:
        # The user wasn't subscribed, so we'll create it.
        sub = Subscription.objects.create(email=request.POST['email'],
                                    newsletter=newsletter)
        send_notification([], [newsletter], request.POST['email'])
    if is_json_request(request):
        return JSONResponse({'success': True, 'message': ''})
    return render_to_response('newsletters/subscribe.html', {
        'newsletter': newsletter
    }, RequestContext(request))

def unsubscribe(request, newsletter_slug):
    """
    Unsubscribe a user from the newsletter.
    
    Requires a POST with an email
    """
    newsletter = get_object_or_404(Newsletter, slug=newsletter_slug)
    if request.method != 'POST':
        if is_json_request:
            return JSONResponse({
                'success': False, 
                'message': 'Only POST methods are allowed.'})
        return HttpResponseNotAllowed(['POST',])
    if 'email' not in request.POST:
        if is_json_request:
            return JSONResponse({
                'success': False, 
                'message': 'No email field was included.'})
        raise Http404("email not included in POST")
    try:
        sub = Subscription.objects.get(email=request.POST['email'],
                                       newsletter=newsletter)
        sub.delete()
        send_notification([newsletter], [], request.POST['email'])
    except Subscription.DoesNotExist:
        pass # The user wasn't subscribed, so just fail gracefully.
    
    if is_json_request(request):
        return JSONResponse({'success': True, 'message': ''})
    return render_to_response('newsletters/unsubscribe.html', {
        'newsletter': newsletter
    }, RequestContext(request))