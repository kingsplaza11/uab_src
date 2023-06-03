from django.contrib import admin
from .models import BankAccount, Transfer, Deposit, Withdrawal, History

admin.site.register(BankAccount)
admin.site.register(Transfer)
admin.site.register(Deposit)
admin.site.register(Withdrawal)
admin.site.register(History)
