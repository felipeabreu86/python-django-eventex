from django.conf import settings
from django.http import Http404, HttpResponseRedirect
from django.core import mail
from django.shortcuts import render, resolve_url as r
from eventex.subscriptions.forms import SubscriptionForm
from django.template.loader import render_to_string
from eventex.subscriptions.models import Subscription


def new(request):
    if request.method == 'POST':
        return create(request)

    return empty_form(request)


def create(request):
    form = SubscriptionForm(request.POST)

    if not form.is_valid():
        return render(request, 'subscriptions/subscription_form.html', {'form': form})

    subscription = Subscription.objects.create(**form.cleaned_data)

    # Send email
    _send_mail(
        'subscriptions/subscription_email.txt',
        {'subscription': subscription},
        'Confirmação de inscrição',
        settings.DEFAULT_FROM_EMAIL,
        subscription.email
    )

    return HttpResponseRedirect(r('subscriptions:detail', subscription.pk))


def empty_form(request):
    context = {'form': SubscriptionForm()}
    return render(request, 'subscriptions/subscription_form.html', context)


def detail(request, pk):
    try:
        subscription = Subscription.objects.get(pk=pk)
    except Subscription.DoesNotExist:
        raise Http404

    context = {'subscription': subscription}
    return render(request, 'subscriptions/subscription_detail.html', context)


def _send_mail(template_name, context, subject, from_, to):
    body = render_to_string(template_name, context)
    mail.send_mail(subject, body, from_, [from_, to])
