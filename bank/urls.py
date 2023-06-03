from django.urls import path
from . import views as bank_views
from . import core
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('' , bank_views.user_dashboard, name='user-dashboard'),
    path('quick-banking/' , bank_views.transfer_money, name='transfer-money'),
    path('quick-banking/success/', bank_views.trf_receipt, name='transfer-receipt'),
    path('deposits', bank_views.deposit_logs, name='deposit-logs'),
    path('withdrawals', bank_views.withdrawal_logs, name='withdrawals-logs'),
    path('account-statement', bank_views.account_statement, name='account-statement'),
    path('py-scheme', bank_views.earn_py_scheme, name='py-scheme'),
    path('account-suspended', bank_views.account_blocked, name='account-suspended'),

    # ===>
    path('transfer-money-func' , core.CashTransfer.transfer_money_func, name='transfer-money-func'),
    path('fetch-transfer-data' , core.CashTransfer.fetch_cash_transfer_data, name='fetch-transfer-data'),
    path('validate-transfer-pin' , csrf_exempt(core.CashTransfer.validate_trf_pin), name='validate-transfer-pin'),
    path('send-trf-otp' , csrf_exempt(core.CashTransfer.send_trf_otp), name='send-trf-otp'),
]