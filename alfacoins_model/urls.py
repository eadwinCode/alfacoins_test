from django.urls import path
from .views import payment_notification, PaymentList, PaymentSetupView, PaymentDetail

urlpatterns = [
    path('payments', PaymentList.as_view(), name="payment_list"),
    path('', PaymentSetupView.as_view(), name="payment_setup"),
    path('payments/<uuid:pk>', PaymentDetail.as_view(), name='payment_detail'),
    path('notification/payments', payment_notification, name='ipn-payment')
]
