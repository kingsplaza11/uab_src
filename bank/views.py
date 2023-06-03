from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from.models import Deposit, Withdrawal, Transfer, History
from django.utils import timezone
from django.contrib import messages
from django.utils.safestring import mark_safe
import datetime
from utils.tools import qr_code_generator
from site_admin.models import Bank
from utils.unique_generators import GenerateUUIDCode

def account_blocked(request):
    return render(request, 'bank/blocked.html')


@login_required
def user_dashboard(request):
    user = request.user
    fullname = str(user.fullname)
    fullname_list = fullname.split()
    today = datetime.datetime.now()
    user_deposits = Deposit.objects.filter(user=user, date__month=today.month)
    user_withdrawals = Withdrawal.objects.filter(user=user, date__month=today.month)
    user_transfers = Transfer.objects.filter(user=user, date__month=today.month)
    total_deposits_list = []
    total_withdrawal_list = []
    total_transfer_list = []

    for i in user_deposits:
        total_deposits_list.append(i.amount)
    for i in user_withdrawals:
        total_withdrawal_list.append(i.amount)
    for i in user_transfers:
        total_transfer_list.append(i.amount)

    ctx  = {
        'page_title': 'Dashboard',
        'username':fullname_list[0],
        'total_deposits_amount': sum(total_deposits_list),
        'total_withdrawal_amount': sum(total_withdrawal_list),
        'total_transfer_amount': sum(total_transfer_list),
        'a_qr_code': qr_code_generator(user.bank_account.account_number),
        'history': History.objects.filter(user=user).order_by('-date')[:3]
    }
    if user.bank_account.blocked:
        return redirect('account-suspended')
    return render(request, 'bank/db.html', ctx)

@login_required
def transfer_money(request):
    user = request.user
    protocol = request.GET.get('protocol')
    ctx = {
        'page_title': 'Transfer Money',
        'trf_protocol':protocol,
        'banks': Bank.objects.all()
    }
    if user.bank_account.blocked:
        return redirect('account-suspended')
    return render(request, 'bank/transfer.html', ctx)

@login_required
def trf_receipt(request):
    user = request.user
    ctx = {
        'txn_id':request.GET.get('txn_id'),
        'fullname':request.GET.get('fullname'),
        'acc_no':request.GET.get('acc_no'),
        'bank':request.GET.get('bank'),
        'amount':request.GET.get('amount')
    }
    if user.bank_account.blocked:
        return redirect('account-suspended')
    return render(request, 'bank/trf-receipt.html', ctx)


@login_required
def deposit_logs(request):
    user = request.user
    logs = Deposit.objects.filter(user=user)
    ctx = {
        'logs':logs,
        'page_title': 'Deposit Logs',
        'today': timezone.now()
    }
    if user.bank_account.blocked:
        return redirect('account-suspended')
    return render(request, 'bank/deposits.html', ctx)

@login_required
def withdrawal_logs(request):
    user = request.user
    logs = Withdrawal.objects.filter(user=user)
    ctx = {
        'logs':logs,
        'page_title': 'Withdrawal Logs',
        'today': timezone.now()
    }
    if user.bank_account.blocked:
        return redirect('account-suspended')
    return render(request, 'bank/withdrawals.html', ctx)


@login_required
def account_statement(request):
    user = request.user
    user_timeline_list = []

    user_timeline = History.objects.filter().order_by('-date')
    for obj in user_timeline:
        user_timeline_list.append(
            {'date': obj.date, 'type': obj.type, 
            'amount': obj.amount, 'ref': GenerateUUIDCode.numeric_uid(8),
            }
        )


    ctx = {
        'page_title': 'Statement of account',
        'bank_account': user.bank_account,
        'history': user_timeline_list,
        'today':timezone.now()
    }
    if user.bank_account.blocked:
        return redirect('account-suspended')
    return render(request, 'bank/account-statement.html', ctx)


@login_required
def earn_py_scheme(request):
    user = request.user
    ctx = {
        'page_title': 'Per Year Scheme',
    }
    if request.method == 'POST':
        messages.error(request, mark_safe(
        f"""
            <h5 class="textColor reduceH5">Request Failed</h5>
            <p>This service is currently unavailable. Visit one of our branches or try again later!</p>
            """  
        ))
        return redirect('py-scheme')
    if user.bank_account.blocked:
        return redirect('account-suspended')
    return render(request, 'bank/py-scheme.html', ctx)