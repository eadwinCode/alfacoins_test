
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from alfacoins_model.utils import create_hash_data, request_handle
from django.http.response import HttpResponseBadRequest
from alfacoins_model.models import Payment
import logging

logger = logging.getLogger(__name__)


# 'coin_received_amount': '0.00000000', 'currency': 'USD',
# 'fiat_paid_amount': '0.000000', 'hash': '920FF89E3520672E391C201BE8207B10,
# 'id': '575965',
# 'modified': '2019-11-17 08:51:01',
# 'order_id': 'a8ce978e-0a9f-414a-9a51-4efd9c2ed49a',
# 'received_amount': '101.00000000',
# 'status': 'expired',
# 'type': 'bitcoin'


@csrf_exempt
def payment_notification(request):
    status = Payment.status_dict()
    post_data = request.POST.dict()
    server_hash = post_data.pop('hash')

    our_hash = create_hash_data(**post_data)

    if our_hash != server_hash:
        return HttpResponseBadRequest('Invalid merchant id')

    payment = get_object_or_404(Payment, provider_tx_id__exact=int(post_data['id']))
    payment.amount_paid = post_data['coin_received_amount']
    payment.status = status.get(post_data['status'])
    logger.info(f"Notification received for #{post_data['id']}")
    payment.save()

    return HttpResponse("OK", content_type="text/plain")


@csrf_exempt
def mark_as_paid(request, tx_id):
    payment = get_object_or_404(Payment, provider_tx_id__exact=tx_id)

    params = dict(
        coin_received_amount='0.00000000',
        currency='USD', fiat_paid_amount='0.000000', hash='920FF89E3520672E391C201BE8207B10',
        id=575965, modified='2019-11-17 08:51:01', order_id='a8ce978e-0a9f-414a-9a51-4efd9c2ed49a',
        status='expired', received_amount='101.00000000', type='bitcoin')

    url = request.build_absolute_uri(reverse("ipn-payment"))
    response = request_handle(url, params=params)
    return response
