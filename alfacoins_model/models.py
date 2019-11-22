from django.db import models
import datetime
from django.utils import timezone
from decimal import Decimal
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel
from .utils.codetype import get_coins_list, get_standard_currency, USD, BTC
import uuid
from alfacoins_model.alfacoin import AlfaCoinsProvider
from .utils import generate_qr_code_url
from django.conf import settings


class CoinPaymentsTransaction(TimeStampedModel):
    id = models.CharField(max_length=100, verbose_name=_('id'), primary_key=True, editable=True)
    address = models.CharField(max_length=150, verbose_name=_('Address'))
    legacy_address = models.CharField(max_length=150, verbose_name=_('Legacy Address'))
    destination_tag = models.CharField(max_length=150, verbose_name=_('Destination Tag'))
    coin_amount = models.FloatField(verbose_name=_('Coin Amount'), default=0)
    coin_received_amount = models.FloatField(verbose_name=_('Coin Received Amount'), default=0)
    status_url = models.URLField(verbose_name=_('Status Url'))
    qr_code = models.URLField(verbose_name=_('QR Code'))

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
    currency_type = models.CharField(max_length=8, choices=get_coins_list(), default=BTC,
                                     verbose_name=_('Currency Type'))
    currency = models.CharField(max_length=8, choices=get_standard_currency(), default=USD,
                                verbose_name=_('Payment currency'))
    amount = models.FloatField(verbose_name=_('Amount'))
    amount_paid = models.FloatField(verbose_name=_('Amount paid'))
    provider_tx = models.OneToOneField(CoinPaymentsTransaction, on_delete=models.CASCADE,
                                       verbose_name=_('Payment transaction'), null=True, blank=True)
    status = models.CharField(max_length=4, choices=PAYMENT_STATUS_CHOICES)

    payerName = models.CharField(max_length=250, null=True, blank=True, verbose_name=_("Customer's name"))
    payerEmail = models.EmailField(null=True, blank=True, verbose_name=_("Customer's email"))
    description = models.TextField(null=True, blank=True, verbose_name=_("Description"))
    timeout = models.DateTimeField(verbose_name=_('Valid until'), editable=False)

    def __str__(self):
        return "{} of {} - {}".format(str(self.amount_paid), str(self.amount),
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
            return self.timeout < timezone.now()

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
        params = dict(amount=self.amount_left(), type=self.currency_type, order_id=str(self.id),
                      description=self.description, currency=self.currency, options=options)

        result = alfacoins.create_order(**params)
        self.timeout = timezone.now() + datetime.timedelta(seconds=int(getattr(settings, 'ALFACOINS_TIMEOUT', '900')))
        deposit = result['deposit']
        data = dict(
            id=result['id'],
            coin_amount=Decimal(result['coin_amount']),
            status_url=result['url'],
            coin_received_amount=float(0),
            qr_code=generate_qr_code_url(f"{self.currency_type.lower()}:"
                                         f"{deposit.get('address')}?amount={result.get('coin_amount')}")
        )
        data.update(**deposit)
        c = CoinPaymentsTransaction.objects.create(**data)

        self.provider_tx = c
        self.save()
        return c

    @classmethod
    def status_dict(cls):
        return {'expired': Payment.PAYMENT_STATUS_EXPIRED, 'paid': Payment.PAYMENT_STATUS_PAID,
                'partially paid': Payment.PAYMENT_STATUS_PARTIAL_PAID, 'new': Payment.PAYMENT_STATUS_NEW,
                'completed': Payment.PAYMENT_STATUS_COMPLETED, 'refund': Payment.PAYMENT_STATUS_REFUND
                }

    def get_order_status(self):
        if self.provider_tx and not (self.status in [Payment.PAYMENT_STATUS_EXPIRED, Payment.PAYMENT_STATUS_COMPLETED]):
            alfacoins = AlfaCoinsProvider.coinsprovider()
            res = alfacoins.order_status(txn_id=int(self.provider_tx.id))
            if self.status != Payment.PAYMENT_STATUS_COMPLETED:
                self.status = self.status_dict().get(res['status'])
                self.amount_paid = float(res['amount'])
                self.provider_tx.coin_received_amount = float(res['coin_received_amount'])
                self.provider_tx.coin_amount = float(res['coin_requested_amount'])
                self.save()
            return dict(status=res['status'], date=res['date'], timeout=str(self.timeout),
                        is_expired=self.is_expired(), coin_requested_amount=self.provider_tx.coin_amount,
                        type=res['type'], coin_received_amount=self.provider_tx.coin_received_amount,
                        rate=float(res['rate']), amount=self.amount, currency=self.currency)

        return dict(status=self.get_status_display(), timeout=str(self.timeout), is_expired=self.is_expired(),
                    amount=self.amount, currency=self.currency)


class WithdrawalTransaction(TimeStampedModel):
    id = models.CharField(max_length=100, verbose_name=_('id'), primary_key=True, editable=True)
    coin_amount = models.FloatField(verbose_name=_('Coin Amount'), null=True, blank=True)
    network_fee = models.FloatField(verbose_name=_('Network Fee'), null=True, blank=True)
    commission = models.FloatField(verbose_name=_('Commission'), null=True, blank=True)
    tx_id = models.CharField(max_length=200, verbose_name=_('tx_id'), editable=True, null=True, blank=True)


class Withdrawal(TimeStampedModel):
    WITHDRAW_STATUS_COMPLETED = 'COMPL'
    WITHDRAW_STATUS_PENDING = 'PEND'
    WITHDRAW_STATUS_NEW = 'NEW'

    WITHDRAW_STATUS_CHOICES = (
        (WITHDRAW_STATUS_COMPLETED, _('Completed')),
        (WITHDRAW_STATUS_PENDING, _('Pending')),
        (WITHDRAW_STATUS_NEW, _('new')),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    address = models.CharField(max_length=150, verbose_name=_('Coin Address'))
    legacy_address = models.CharField(null=True, blank=True, max_length=150, verbose_name=_('Legacy Address'))
    destination_tag = models.CharField(null=True, blank=True, max_length=150, verbose_name=_('Destination Tag'))

    amount = models.FloatField(verbose_name=_('Amount'))
    coin_amount = models.FloatField(null=True, blank=True, verbose_name=_('Coin Amount'))
    currency_type = models.CharField(max_length=8, choices=get_coins_list(), default=BTC,
                                     verbose_name=_('Currency Type'))
    recipient_name = models.CharField(max_length=250, null=True, blank=True, verbose_name=_("Customer's name"))
    recipient_email = models.EmailField(null=True, blank=True, verbose_name=_("Customer's email"))
    reference = models.TextField(null=True, blank=True, verbose_name=_("Description"))
    status = models.CharField(max_length=4, choices=WITHDRAW_STATUS_CHOICES)
    provider_tx = models.OneToOneField(WithdrawalTransaction, on_delete=models.CASCADE,
                                       verbose_name=_('Withdrawal transaction'), null=True, blank=True)

    approved = models.BooleanField(default=False, verbose_name=_('Approved'), editable=False)

    def __str__(self):
        return f"Paid {self.amount or self.coin_amount} to {self.address} {self.currency_type}"

    @classmethod
    def status_dict(cls):
        return {'pending': Withdrawal.WITHDRAW_STATUS_PENDING, 'completed': Withdrawal.WITHDRAW_STATUS_COMPLETED, 'new': Withdrawal.WITHDRAW_STATUS_NEW}

    def create_wx(self, **kwargs):
        """
        :param kwargs:
            address           for Bitcoin, Litecoin, Ethereum, Dash
            destination_tag   for Bitcoin Cash
            legacy_address    for XRP
        :return: `WithdrawalTransaction` instance
        """
        alfacoins = AlfaCoinsProvider.coinsprovider()
        if self.coin_amount and self.amount:
            raise Exception('coin_amount and amount can not be used at the same time')

        options = dict(address=self.address)
        if self.destination_tag:
            options.update(destination_tag=self.destination_tag)
        if self.legacy_address:
            options.update(legacy_address=self.legacy_address)
        options.update(**kwargs)
        params = dict(amount=str(self.amount), type=self.currency_type, coin_amount=self.coin_amount,
                      reference=self.reference, recipient_name=self.recipient_name, options=options,
                      recipient_email=self.recipient_email)

        result = alfacoins.bitsend(**params)
        c = WithdrawalTransaction.objects.create(id=result)

        self.provider_tx = c
        self.save()
        return c

    def get_wx_status(self):
        if self.provider_tx and self.status != Withdrawal.WITHDRAW_STATUS_COMPLETED:
            alfacoins = AlfaCoinsProvider.coinsprovider()
            res = alfacoins.bitsend_status(bitsend_id=int(self.provider_tx.id))
            self.status = self.status_dict().get(res['status'])
            self.provider_tx.tx_id = res.get('txid', None)
            self.provider_tx.coin_amount = float(res.get('coin_amount', 0))
            self.provider_tx.network_fee = float(res.get('network_fee', 0))
            self.provider_tx.commission = float(res.get('commission', 0))
            self.save()
            return dict(status=res['status'], type=res['type'], coin_amount=float(res['coin_amount']))

        return dict(status=self.get_status_display(), type=self.currency_type,
                    coin_amount=self.provider_tx.coin_amount)
