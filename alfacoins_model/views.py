from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, FormView, DetailView

from .utils import create_hash_data
from django.http.response import HttpResponseBadRequest
from .models import Payment
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

# Create your views here.
@csrf_exempt
def payment_notification(request):
    post_data = request.POST.dict()
    server_hash = post_data.pop('hash')

    our_hash = create_hash_data(**post_data)

    if our_hash != server_hash:
        return HttpResponseBadRequest('Invalid merchant id')

    return HttpResponse("OK", content_type="text/plain")


class ExamplePaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'currency_type', 'currency', 'description']


def create_tx(request, payment):
    context = {}
    try:
        tx = payment.create_tx()
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
