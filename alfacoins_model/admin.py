from django.contrib import admin
from .models import Withdrawal, WithdrawalTransaction
# Register your models here.

admin.site.register(Withdrawal)
admin.site.register(WithdrawalTransaction)