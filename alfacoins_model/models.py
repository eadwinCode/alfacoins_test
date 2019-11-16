from django.db import models
import datetime
from django.utils import timezone
from decimal import Decimal
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel
from .utils.codetype import get_coins_list, get_standard_currency, USD, BTC
import uuid
from django.utils.functional import cached_property
from alfacoins_model.alfacoin import AlfaCoinsProvider


class CoinPaymentsTransaction(TimeStampedModel):
    id = models.CharField(max_length=100, verbose_name=_('id'), primary_key=True, editable=True)
    address = models.CharField(max_length=150, verbose_name=_('Address'))
    amount = models.FloatField(max_digits=65, decimal_places=18, verbose_name=_('Amount'))
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
    currency_type = models.CharField(max_length=8, choices=get_coins_list(), default=BTC, verbose_name=_('Currency Type'))
    currency = models.CharField(max_length=8, choices=get_standard_currency(), default=USD,
                                verbose_name=_('Payment currency'))
    amount = models.FloatField(max_digits=65, decimal_places=18, verbose_name=_('Amount'))
    amount_paid = models.FloatField(max_digits=65, decimal_places=18, verbose_name=_('Amount paid'))
    provider_tx = models.OneToOneField(CoinPaymentsTransaction, on_delete=models.CASCADE,
                                       verbose_name=_('Payment transaction'), null=True, blank=True)
    status = models.CharField(max_length=4, choices=PAYMENT_STATUS_CHOICES)

    payerName = models.CharField(max_length=250, null=True, blank=True, verbose_name=_("Customer's name"))
    payerEmail = models.EmailField(null=True, blank=True, verbose_name=_("Customer's email"))
    description = models.TextField(null=True, blank=True, verbose_name=_("Description"))

    def __str__(self):
        return "{} of {} - {}".format(str(self.amount_paid.normalize()), str(self.amount.normalize()),
                                      self.get_status_display())

    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')

    def is_paid(self):
        return self.status == self.PAYMENT_STATUS_PAID

    def amount_left(self):
        value_ = self.amount - self.amount_paid
        return value_

    def is_expired(self):
        if self.provider_tx:
            return self.provider_tx.timeout < timezone.now()

   

    def create_tx(self, **kwargs):
        """
        :param kwargs:
            payerEmail   Optionally (but highly recommended) Customer's email for notification.
            payerName    Optionally Customer's name for notification.

            notificationURL      Optionally custom Merchant's URL for payment notification.
            redirectURL          Optionally Merchant's page which is shown after payment is made by a customer
        :return: `CoinPaymentsTransaction` instance
        """
        alfacoins = AlfaCoinsProvider.coinsprovider()
        options = dict(payerName=self.payerName, payerEmail=self.payerEmail)
        options.update(**kwargs)
        params = dict(amount=self.amount_left().normalize(), type=self.currency_type, order_id=self.id, 
        description=self.description, currency=self.currency, options=options)

        result = alfacoins.create_order(**params)
        if result['error'] == 'ok':
            result = result['result']
            timeout = timezone.now() + datetime.timedelta(seconds=result['timeout'])
            c = CoinPaymentsTransaction.objects.create(id=result['id'],
                                                       amount=Decimal(result['coin_amount']),
                                                       address=result['deposit'],
                                                       iframe_url=result['iframe'],
                                                       status_url=result['url'],
                                                       timeout=timeout)
            self.provider_tx = c
            self.save()
        else:
            return None

        return c

