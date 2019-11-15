from django.db import models
import datetime
from decimal import Decimal
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel
from .utils.codetype import get_coins_list, get_standard_currency, USD, BTC
import uuid


class CoinPaymentsTransaction(TimeStampedModel):
    id = models.CharField(max_length=100, verbose_name=_('id'), primary_key=True, editable=True)
    address = models.CharField(max_length=150, verbose_name=_('Address'))
    amount = models.DecimalField(max_digits=65, decimal_places=18, verbose_name=_('Amount'))
    confirms_needed = models.PositiveSmallIntegerField(verbose_name=_('Confirms needed'))
    iframe_url = models.URLField(verbose_name=_('iframe Url'))
    status_url = models.URLField(verbose_name=_('Status Url'))
    timeout = models.DateTimeField(verbose_name=_('Valid until'))

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = _('CoinPayments Transaction')
        verbose_name_plural = _('CoinPayments Transactions')


class Payment(TimeStampedModel):
    PAYMENT_STATUS_PAID = 'PAID'
    PAYMENT_STATUS_EXPIRED = 'EXPR'
    PAYMENT_STATUS_REFUND = 'REF'
    PAYMENT_STATUS_COMPLETED = 'COMPL'
    PAYMENT_STATUS_NEW = 'NEW'
    PAYMENT_STATUS_PARTIAL_PAID = 'PPD'

    PAYMENT_STATUS_CHOICES = (
        (PAYMENT_STATUS_NEW, _('New')),
        (PAYMENT_STATUS_COMPLETED, _('Completed')),
        (PAYMENT_STATUS_PARTIAL_PAID, _('Partially paid')),
        (PAYMENT_STATUS_REFUND, _('Refunded')),
        (PAYMENT_STATUS_EXPIRED, _('Expired')),
        (PAYMENT_STATUS_PAID, _('Paid'))
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=8, choices=get_coins_list(), default=BTC, verbose_name=_('Currency Type'))
    currency = models.CharField(max_length=8, choices=get_standard_currency(), default=USD,
                                verbose_name=_('Payment currency'))
    amount = models.DecimalField(max_digits=65, decimal_places=18, verbose_name=_('Amount'))
    amount_paid = models.DecimalField(max_digits=65, decimal_places=18, verbose_name=_('Amount paid'))
    provider_tx = models.OneToOneField(CoinPaymentsTransaction, on_delete=models.CASCADE,
                                       verbose_name=_('Payment transaction'), null=True, blank=True)
    status = models.CharField(max_length=4, choices=PAYMENT_STATUS_CHOICES)

    payerName = models.CharField(max_length=250, null=True, blank=True, verbose_name=_("Customer's name"))
    payerEmail = models.EmailField(null=True, blank=True, verbose_name=_("Customer's email"))
    description = models.TextField(null=True, blank=True, verbose_name=_("Description"))


