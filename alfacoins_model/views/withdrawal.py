import json
from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse
from django import forms
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, FormView, DetailView
from django.conf import settings
from alfacoins_model.utils import create_hash_data, request_handle
from django.http.response import HttpResponseBadRequest
from alfacoins_model.models import Withdrawal
import logging

logger = logging.getLogger(__name__)


class ExampleWithdrawalForm(forms.ModelForm):
    class Meta:
        model = Withdrawal
        fields = ['amount', 'address', 'currency_type', 'recipient_email', 'recipient_name', 'reference']


def create_wx(request, withdrawal):
    context = {}
    try:
        tx = withdrawal.create_wx()
        withdrawal.status = Withdrawal.WITHDRAW_STATUS_PENDING
        withdrawal.save()
        context['object'] = withdrawal
    except Exception as e:
        context['error'] = e
    return render(request, 'alfacoins_model/withdraw_detail.html', context)


class WithdrawList(ListView):
    model = Withdrawal
    template_name = 'alfacoins_model/withdraw_list.html'


class WithdrawDetail(DetailView):
    model = Withdrawal
    template_name = 'alfacoins_model/withdraw_detail.html'
    context_object_name = 'object'


class WithdrawSetupView(FormView):
    template_name = 'alfacoins_model/withdraw_setup.html'
    form_class = ExampleWithdrawalForm

    def form_valid(self, form):
        cl = form.cleaned_data
        withdraw = form.save(commit=False)
        return create_wx(self.request, withdraw)


def get_bit_send_status(request, tx_id):
    withdraw = get_object_or_404(Withdrawal, provider_tx_id__exact=tx_id)
    return HttpResponse(json.dumps(withdraw.get_wx_status(), indent=4), content_type='application/json')
