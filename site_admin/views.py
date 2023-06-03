from django.shortcuts import render
from account.models import Account
from bank.models import Withdrawal, Deposit, History
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.shortcuts import redirect
from utils.unique_generators import GenerateUUIDCode
from site_admin.models import Bank
from .models import Support
from django.conf import settings as site_settings
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string


def users(request):
    ctx = {
        'accounts': Account.objects.all().order_by('-date_joined'),
        'page_title':'User Accounts',
        'banks':Bank.objects.all(),
        'page_title': 'Registered Accounts'
    }
    return render(request, 'sa/users.html', ctx)


def user_detail(request, pk):
    target_user =  Account.objects.get(pk=pk)

    c_box_data = { False: 'checked', True: ''}
    c_box_data_or = { False: '', True: 'checked'}
    login_blocked = c_box_data[target_user.is_active]
    bank_blocked = c_box_data_or[target_user.bank_account.blocked]

    ctx = {
        'tu': target_user,
        'page_title': target_user.fullname + ' - ' + target_user.email,
        'bank_blocked': bank_blocked,
        'login_blocked': login_blocked
    }
    return render(request, 'sa/user-detail.html', ctx)

def create_logs_view(request):
    ctx = {
        'page_title': 'Create Logs',
        'account_options': Account.objects.all()
    }
    return render(request, 'sa/create-logs.html', ctx)


def fund_account(request, pk):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        amount = float(amount)
        target_account = Account.objects.get(pk=pk)
        target_account.bank_account.balance = amount
        target_account.bank_account.save(update_fields = ['balance'])

        messages.success(request, mark_safe(
            f"""
                <h5 class="textColor reduceH5"><b>Done!</b></h5>
                <p class="moreBlack">
                    Account balance was updated successfully
                </p>
            """
            ))
        return redirect('users')
    return redirect('users')


def create_logs(request):
    if request.method == 'POST':
        log_type = request.POST.get('log_type')
        account = request.POST.get('account')
        amount = request.POST.get('amount')
        method = request.POST.get('method')
        if log_type == 'deposit':
            description = request.POST.get('description')
            Deposit.objects.create(
                user = Account.objects.get(email=account),
                amount = amount,
                method = method,
                status = 'successful',
                description = description,
                reference_id = GenerateUUIDCode.alpha_numeric_uid(11)
            )
            t_u = Account.objects.get(email=account),
            History.objects.create( user=t_u, amount = amount, type = 'received')
        if log_type == 'withdrawal':
            Withdrawal.objects.create(
                user = Account.objects.get(email=account),
                amount = amount,
                method = method,
                status = 'successful',
                reference_id = GenerateUUIDCode.alpha_numeric_uid(11)
            )
            t_u = Account.objects.get(email=account),
            History.objects.create( user=t_u, amount = amount, type = 'withdrawal' )
        messages.success(request, mark_safe(
            f"""
                <h5 class="textColor reduceH5"><b>Done!</b></h5>
                <p class="moreBlack">
                    Logs was create successfully
                </p>
            """
        ))
        return redirect('create-logs-view')
    return redirect('create-logs-view')


def impose_restrictions(request):
    if request.method == 'POST':
        target_account = request.POST.get('target_account')
        bank_blocked = request.POST.get('bank-blocked')
        login_blocked = request.POST.get('login-blocked')

        # get on None checkbox data
        checkbox_value = { 'on': False, None: True }
        checkbox_value_or = { 'on': True, None: False }

        target_user = Account.objects.get(email=target_account)
        target_user.is_active = checkbox_value[login_blocked]
        target_user.bank_account.blocked = checkbox_value_or[bank_blocked]
        target_user.bank_account.save(update_fields=['blocked'])
        target_user.save(update_fields=['is_active'])
        messages.success(request, mark_safe(
            f"""
                <h5 class="textColor reduceH5"><b>Done!</b></h5>
                <p class="moreBlack">
                    Changes applied successfully to user account
                </p>
            """
        ))
        return redirect('user-detail', target_user.pk)
    return redirect('users')


def add_bank(request):
    if request.method == 'POST':
        bank_name = request.POST.get('bank-name')
        bank_exists = Bank.objects.filter(name=bank_name).exists()

        if not bank_exists:
            Bank.objects.create(
                name=bank_name
            )
            messages.success(request,
                mark_safe(
                    f"""
                        <h5 class="textColor reduceH5"><b>Done!</b></h5>
                        <p class="moreBlack">
                            Bank Added Successfully
                        </p>
                    """
                )
            )
            return redirect('users')
        else:
            messages.info(request,
                mark_safe(
                    f"""
                        <h5 class="textColor reduceH5"><b>Aborted!</b></h5>
                        <p class="moreBlack">
                            Bank was already created!
                        </p>
                    """
                )
            )
            return redirect('users')
    return redirect('users')


def create_account_admin(request):
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        region = request.POST.get('region')
        password1 = request.POST.get('password1')
        bank = request.POST.get('bank')

        new_user = Account.objects.create(
            fullname = fullname,
            country = region,
            email = email.lower(),
            password=password1, 
        )        
        new_user.set_password(password1)    
        new_user.save()
        # set bank
        if bank != 'uab':
            new_user.bank_account.bank = bank
            new_user.bank_account.save(update_fields=['bank'])
        messages.success(request,
                mark_safe(
                    f"""
                        <h5 class="textColor reduceH5"><b>Account created!</b></h5>
                        <p class="moreBlack">
                            Account was successfully created
                        </p>
                    """
                )
            )
        return redirect('users')


def banks_created(request):
    ctx = {
        'banks_created': Bank.objects.all(),
        'page_title': 'Added Banks'
    }
    return render(request, 'sa/banks.html', ctx)



def delete_account(request, id):
    if request.method == 'POST':
        target_user  = Account.objects.get(pk=id)

        target_user.delete()
        
        messages.success(request, 'Account has been deleted!')
        return redirect('users')


def support_message(request):
    ctx = {
        'page_title': 'Support Messages',
        'requests': Support.objects.filter(status='open').order_by('-date_created')
    }
    return render(request, 'sa/support-message.html', ctx)


def close_support_request(request, id):
    if request.method == 'POST':
        target_request = Support.objects.get(pk=id)
        target_request.status = 'closed'
        target_request.save(update_fields=['status'])
        messages.success(request, mark_safe(
            f"""
                <h5 class="textColor reduceH5"><b>Done!</b></h5>
                <p class="moreBlack">
                    Request closed successfully
                </p>
            """
        ))
        return redirect('close-ticket')


def send_mails(request):
    if request.method == 'POST':
        recipient = request.POST.get('recipient')
        message = request.POST.get('message')
        title = request.POST.get('title')

        # send email
        recipient = recipient
        mail_from = site_settings.DEFAULT_FROM_MAIL
        mail_heading = f'{title}'
        mail_ctx = { 'message':message, 'title':title }
        html_content = render_to_string("emails/admin-mail.html", mail_ctx)
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(
            mail_heading, text_content, mail_from, [recipient]
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send(fail_silently=True)
        # End Email
    ctx = {
        'page_title': 'Admin Mail'
    }
    return render(request, 'sa/send-mail.html', ctx)