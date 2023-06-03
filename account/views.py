from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from .models import Account
from django.utils.safestring import mark_safe
from utils.unique_generators import generate_token

from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.conf import settings as site_settings
from django.template.loader import render_to_string
from django.utils import timezone
import random



def signup_view(request):
    ctx = {
        'title' : 'Create account'
    }
    return render(request, 'account/signup.html', ctx)


def login_view(request):
    next_url = request.GET.get('next')
    ctx = {
        'title' : 'Login',
        'next_url':next_url
    }
    return render(request, 'account/login.html', ctx)


def validate_login_data(request):
    if request.method == 'POST':
        email = request.POST.get('user-email')
        password = request.POST.get('password')
        login_object = auth.authenticate(email=email.lower(), password=password)

        # check if user account is inactive
        user_account_le = Account.objects.get(email=email)
        if user_account_le.is_active == False:
            emit_data = { 
                'status':'login_unauthorized', 
                'message': 'For additional information, send an email to help@unitedassetssavings.com', 
            }
            return JsonResponse(emit_data, safe=False)
        # -------

        if login_object is not None:
            user_account_tbl = Account.objects.get(email=email)
            user_phrase_word = user_account_tbl.pass_phrase
            emit_data = { 'status':'login_ok', 'message': 'login verified', 'phrase_word': user_phrase_word }
        else:
            emit_data = { 'status':'error', 'message': 'Invalid email or password' }
        return JsonResponse(emit_data, safe=False)


def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('user-email')
        password = request.POST.get('password')
        nxt_url = request.POST.get('next-url')
        login_object = auth.authenticate(email=email.lower(), password=password)
        if login_object is not None:
            auth.login(request, login_object)
            if nxt_url != '' and nxt_url is not None and nxt_url != 'None':
                return redirect(nxt_url)
            else:
                return redirect('user-dashboard')
        else:
            return JsonResponse('Unknown Error!', safe=False)
    return redirect('login-view')

# -----------------
# -----------------
def create_user_secret_phrase():
    phrase_list = [
        "stack", "milk", "rocks", "easy", "slay", "elite", "random", "green", "carry", "gloom",
        "plant", "drop", "dew", "enquire", "exceed", "birth", "celebrate", "tree", "rainy", "pass",
        "success", "fly", "grey", "watch", "move", "peep", "sundown", "morning", "good" 
    ]

    p_1 = random.choice(phrase_list)
    p_2 = random.choice(phrase_list)
    p_3 = random.choice(phrase_list)
    return p_1+ '+' + p_2 + '+' + p_3

class UserAccountsViews:

    def check_unique_email(request):
        email = request.POST['email']
        email_exists = Account.objects.filter(email=email).exists()
        if email_exists:
            data_emit = {
                'status':'email_error',
                'message': 'This email is already associated with another account!'
            }
            return JsonResponse(data_emit, safe=False)
        if not email_exists:
            token = generate_token(6)
            # send email
            recipient = email
            from_email = 'noreply@dubicodes.xyz'
            mail_heading = f'Verification Code'
            mail_ctx = {
                'code':token
            }
            html_content = render_to_string("emails/email-verification-code.html", mail_ctx)
            text_content = strip_tags(html_content)
            msg = EmailMultiAlternatives(
                mail_heading, text_content, from_email, [recipient]
            )
            msg.attach_alternative(html_content, 'text/html')
            msg.send()
            # msg.send(fail_silently=True)
            # End Email

            data_emit = {
                'status':'unique_email_success',
                'token': token
            }
            return JsonResponse(data_emit, safe=False)

    def create_user_account(request):
        if request.method == 'POST':
            fullname = request.POST.get('fullname')
            email = request.POST.get('email')
            region = request.POST.get('region')
            password1 = request.POST.get('password1')
            phone_number = request.POST.get('phone_number')

            new_user = Account.objects.create(
                fullname = fullname,
                country = region,
                email = email.lower(),
                password=password1, 
                pass_phrase= create_user_secret_phrase(),
                phone_number = phone_number
            )        
            new_user.set_password(password1)    
            new_user.save()
            # log user in
            """check that new user created successfully"""
            check_new_user = Account.objects.filter(email=new_user.email).exists()
            if check_new_user:
                auth_object = auth.authenticate(email=new_user.email.lower(), password=password1)
                if auth_object is not None:
                    auth.login(request, auth_object)
                    return redirect('account-security')
            else:
                return redirect('login')
            
# ----------------------------------
# ----------------------------------

@login_required
def user_profile(request):
    user = request.user
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        address = request.POST.get('address')
        region = request.POST.get('region')
        user.fullname = fullname
        user.country = region
        user.address = address
        user.save(update_fields = ['fullname', 'address', 'country'])
        messages.success(request, mark_safe(
          f"""
            <h5 class="textColor reduceH5">Profile updated successfully</h5>
            """  
        ))
        return redirect('profile')
    secret_word = user.pass_phrase
    le = secret_word.replace('+', ' ')
    ctx = {
        'page_title': 'Account Details',
        'sw':le
    }

    return render(request, 'account/profile.html', ctx)


@login_required
def set_transfer_pin(request):
    if request.method == 'POST':
        user = request.user
        pin = request.POST.get('pin1')

        if user.bank_account.transfer_pin != '----':
            old_pin = request.POST.get('old_pin')
            # check pin match
            if old_pin != user.bank_account.transfer_pin:
                messages.error(request, mark_safe(
                    f"""<h5 class="textColor reduceH5">Old pin is incorrect. check and retry!</h5>"""
                ))
                return redirect('user-dashboard')
            user.bank_account.transfer_pin = pin
            user.bank_account.save(update_fields=['transfer_pin'])
        else:
            user.bank_account.transfer_pin = pin
            user.bank_account.save(update_fields=['transfer_pin'])
        messages.success(request, mark_safe(
            f"""<h5 class="textColor reduceH5">Pin setup successful!</h5>"""
        ))
        # return redirect('user-dashboard')
    return redirect('user-dashboard')





@login_required
def change_password(request):
    current_password_entered = request.POST['cPassword']
    new_password = request.POST['newPassword']
    confirm_new_password = request.POST['cnewPassword']
    if request.method == 'POST':
        user = request.user
        user_current_password = user.password
        match_check = check_password(current_password_entered, user_current_password)
        if match_check:
            if new_password == confirm_new_password:
                if len(new_password) < 8:
                    messages.info(request, mark_safe(
                        f"""
                            <h5 class="greyWhite">request Failed!</h5>
                            <p class="moreBlack">
                                Your password must be at least 8 characters. <br>
                                Check and try again
                            </p>
                        """
                    ))
                    return redirect('user-dashboard')
                else:
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, mark_safe(
                        f"""
                            <h5 class="greyWhite"><b>Password updated!</b></h5>
                            <p class="moreBlack">
                                Your password has been changed successfully. <br>
                                Continue to login with your newly created password
                            </p>
                        """
                    ))
                    return redirect('login-view')
            else:
                messages.info(request, mark_safe(
                    f"""
                        <h5 class="greyWhite">request Failed!</h5>
                        <p class="moreBlack">
                            The Two passwords do not match. <br>
                            Check and try again
                        </p>
                    """
                    ))
                return redirect('user-dashboard')
        else:
            messages.info(request, mark_safe(
                f"""
                    <h5 class="greyWhite">request Failed!</h5>
                    <p class="moreBlack">
                        The Old password you entered is incorrect. <br>
                        Check and try again
                    </p>
                """
                ))
            return redirect('user-dashboard')

    return redirect('user-dashboard')


@login_required
def account_security_notice(request):
    secret_word = request.user.pass_phrase
    le = secret_word.replace('+', ' ')
    return render(request, 'account/account-security-note.html', {'p_word': le})


def set_profile_photo(request):
    user = request.user
    if request.method == 'POST':
        photo = request.FILES['photo']
        user.photo = photo
        user.save(update_fields = ['photo'])
        messages.success(request, mark_safe(
            f"""
                <h5 class="primary-color">Updated!</h5>
                <p class="moreBlack xsmall">
                    Your account photo has been updated successfully.
                </p>
            """
            ))
        return redirect('profile')
    return redirect('profile')