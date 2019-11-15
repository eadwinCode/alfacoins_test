from django.urls import path
from .views import payment_notification, PaymentList, PaymentSetupView

urlpatterns = [
    path('payments', PaymentList.as_view(), name="payment_list"),
    path('', PaymentSetupView.as_view(), name="payment_setup"),
    path('notification/payments', payment_notification, name='ipn-payment')
]
