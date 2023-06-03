from .models import BankAccount, Transfer, History, Withdrawal
from account.models import Account
from django.http import JsonResponse
from utils.unique_generators import generate_token, GenerateUUIDCode
from django.shortcuts import redirect
import urllib
from django.contrib import messages
from django.utils.safestring import mark_safe

from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.conf import settings as site_settings
from django.template.loader import render_to_string
from django.utils import timezone

from forex_python.converter import CurrencyRates


class CashTransfer:
    def fetch_cash_transfer_data(request):
        beneficiary_acc_no = request.POST.get('beneficiary')
        if beneficiary_acc_no == request.user.bank_account.account_number:
            response = {
                'status':'error',
                'message': 'Invalid Request. Account number error!'
            }
            return JsonResponse(response, safe=False)
        try:
            beneficiary_data = BankAccount.objects.get(account_number = beneficiary_acc_no)
            beneficiary_account = Account.objects.get(email=beneficiary_data.user.email)
            response = {
                'status':'ok',
                'beneficiary_name': beneficiary_account.fullname,
                'beneficiary_acc_no': beneficiary_acc_no,
                'user_fullname': request.user.fullname
            }
        except:
            response = {
                'status':'error',
                'message':  'Encountered error! Invalid Account. Please check that the recipients account number is correct'
            }
        return JsonResponse(response, safe=False)

    # =========================

    def transfer_money_func(request):
        user = request.user
        if request.method == 'POST':
            amount = request.POST.get('amount')
            amount = float(amount)
            beneficiary = request.POST.get('beneficiary')
            bank = request.POST.get('bank')
            user_bank = user.bank_account
            currency = request.POST.get('currency')

            reference_id = GenerateUUIDCode.alpha_numeric_uid(11)

            # TRANSFER TO OWN BANK
            if bank == 'United Assets Savings':
                beneficiary_bank_data = BankAccount.objects.get(account_number = beneficiary)
                beneficiary_account = Account.objects.get(email=beneficiary_bank_data.user.email)
                trf_to = beneficiary_account.fullname
                trf_from = user.fullname

                # perform trx
                user_bank.balance -= amount
                beneficiary_bank_data.balance += amount
                user_bank.save(update_fields = ['balance'])
                beneficiary_bank_data.save(update_fields = ['balance'])

                # update DB
                Transfer.objects.create( user = user, amount = amount, trf_from = trf_from, trf_to = trf_to,
                    status = 'successful', reference_id = reference_id
                )
                # Create history
                History.objects.create( user=user, amount = amount, type = 'sent' )
                History.objects.create( user=beneficiary_account, amount = amount, type = 'received' )
                # create withdrawal log
                Withdrawal.objects.create(
                    user=user, amount = amount, reference_id = GenerateUUIDCode.alpha_numeric_uid(10),
                    status = 'completed', method='Cash Transfer'
                )
                ctx = { 
                    'txn_id':reference_id, 'fullname':trf_to, 'acc_no':beneficiary, 'bank':bank,
                    'amount': amount
                }
                uri = urllib.parse.urlencode(ctx)
                full_url = '/core/quick-banking/success/' + "?" + uri
                return redirect(full_url)

            # TRANSFER TO OTHER BANK
            elif bank != 'United Assets Savings':
                # convert currency
                deduct_amount = amount if currency == 'USD' else convert_currency(currency, amount)
                # ==>
                account_name = request.POST.get('account-name')
                user_bank.balance -= deduct_amount
                user_bank.save(update_fields=['balance'])
                Transfer.objects.create( user=user, amount=deduct_amount, trf_from=user.fullname, trf_to=account_name,
                    status = 'successful', reference_id = reference_id
                )
                History.objects.create( user=user, amount=amount, type='sent' )
                # create withdrawal log
                Withdrawal.objects.create(
                    user=user, amount = deduct_amount, reference_id = GenerateUUIDCode.alpha_numeric_uid(10),
                    status = 'completed', method='Cash Transfer'
                )
                messages.success(request, mark_safe(
                    f"""
                    <h5 class="primary-color boldText reduceH5">Successful!</h5>
                    <p class="xsmall">Your transfer request of <b>{amount}0 {currency}</b> was successful.</p>
                    <p class="xsmall">Exchange rates are applied accordingly when sending in other currencies. Contact our support team for more enquiries</p>
                    """ 
                ))
                return redirect('user-dashboard')
        # if request not POST
        return redirect('transfer-money')

    
    def validate_trf_pin(request):
        if request.method == 'POST':
            provided_pin = request.POST.get('trf-pin')
            user = request.user
            user_trf_pin = user.bank_account.transfer_pin
            if user_trf_pin == provided_pin:
                res = { 'status':'success' }
            else:
                res = { 'status':'error' }
            return JsonResponse(res, safe=False)

    def send_trf_otp(request):
        if request.method == 'POST':
            trf_otp = generate_token(5)
            res = {
                'status':'ok',
                'trf_otp': trf_otp
            }
            return JsonResponse(res, safe=False)


def convert_currency(currency, amount):
    c_converter = CurrencyRates()
    currency_value = c_converter.convert('USD', currency, amount)
    return currency_value
