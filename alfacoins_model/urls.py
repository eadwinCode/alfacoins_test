from django.urls import path
from .views import payment_notification

urlpatterns = [
    path('notification/payments', payment_notification, name='ipn-payment')
]
