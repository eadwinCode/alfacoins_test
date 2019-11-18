import json
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django import forms
from django.urls import reverse
from django.views.generic import ListView, FormView, DetailView
from django.conf import settings
from alfacoins_model.models import Payment
import logging

logger = logging.getLogger(__name__)


class ExamplePaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'currency_type', 'currency', 'description']


def create_tx(request, payment):
    context = {}
    try:
        notification_url = None
        if not getattr(settings, 'DEBUG', True):
            notification_url = request.\
                build_absolute_uri(reverse(getattr(settings, 'ALFACOINS_NOTIFICATION_URL', 'ipn-payment')))
        tx = payment.create_tx(notificationURL=notification_url)
        payment.status = Payment.PAYMENT_STATUS_NEW
        payment.save()
        context['object'] = payment
    except Exception as e:
        context['error'] = e
    return render(request, 'alfacoins_model/payment_detail.html', context)


class PaymentList(ListView):
    model = Payment
    template_name = 'alfacoins_model/payment_list.html'


class PaymentDetail(DetailView):
    model = Payment
    template_name = 'alfacoins_model/payment_detail.html'
    context_object_name = 'object'


class PaymentSetupView(FormView):
    template_name = 'alfacoins_model/payment_setup.html'
    form_class = ExamplePaymentForm

    def form_valid(self, form):
        cl = form.cleaned_data
        payment = form.save(commit=False)
        payment.amount_paid = float(0)
        return create_tx(self.request, payment)


def get_order_status(request, tx_id):
    payment = get_object_or_404(Payment, provider_tx_id__exact=tx_id)
    return HttpResponse(json.dumps(payment.get_order_status(), indent=4), content_type='application/json')
