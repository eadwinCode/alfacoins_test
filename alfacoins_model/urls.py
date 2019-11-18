from django.urls import path
from django.conf import settings
from .views import (
    payment_notification, mark_as_paid,

)
from .views.payments import PaymentList, PaymentSetupView, PaymentDetail, get_order_status
from .views.withdrawal import WithdrawList, WithdrawDetail, WithdrawSetupView, get_bit_send_status


# payments
urlpatterns = [
    path('payments', PaymentList.as_view(), name="payment_list"),
    path('', PaymentSetupView.as_view(), name="payment_setup"),
    path('payments/<uuid:pk>', PaymentDetail.as_view(), name='payment_detail'),
    path('payment/<str:tx_id>/status', get_order_status, name='order_status')
]

if getattr(settings, 'DEBUG', False):
    urlpatterns += [
        path('debug/<str:tx_id>', mark_as_paid, name='mark_as_paid'),
    ]

# ipn view
urlpatterns += [
    path('notification/payments', payment_notification, name='ipn-payment'),
]

# withdraws
urlpatterns += [
    path('withdrawals', WithdrawList.as_view(), name="withdraw_list"),
    path('withdrawals/new', WithdrawSetupView.as_view(), name="withdraw_setup"),
    path('withdrawals/<uuid:pk>', WithdrawDetail.as_view(), name='withdraw_detail'),
    path('withdrawals/<str:tx_id>/status', get_bit_send_status, name='bit_send_status')
]
