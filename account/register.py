from django.shortcuts import redirect, render
from .models import Account
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.conf import settings
from django.template.loader import render_to_string


def create_account(request):
    if request.method == 'POST':
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        ref_id = request.POST['ref_id']
        country = request.POST['country']

        userExists = Account.objects.filter(email=email)
        passwordLimitedValid = len(password1) >= 8


        if password1 == password2:
            passwordMatch = True
        else:
            passwordMatch = False
        if userExists:
            messages.info(request, mark_safe(
            """
            <div class="mt-4">
                <h5>Encountered Error!</h5>
                <p class="greyWhite messageText">
                    This email is already associated with another account
                </p>
                <p class="redText">Please correct the errors to proceed</p>
            </div>
            """
            ))
            ctx = {
                'email':email, 
                'first_name':first_name, 
                'last_name':last_name,
                'ref_code':ref_id,
            }
            return render(request, 'auth/register.html', ctx)
        # ******>

        if not passwordLimitedValid:
            messages.info(request, mark_safe(
            """
            <div class="mt-4">
                <h5>Password Error!</h5>
                <p class="greyWhite messageText">
                    Password must be atleast 8 Characters
                </p>
                <p class="redText">Please correct the errors to proceed</p>
            </div>
            """
            ))
            ctx = {
                'email':email, 
                'first_name':first_name, 
                'last_name':last_name,
                'ref_code':ref_id,
            }
            return render(request, 'auth/register.html', ctx)

        # ******>

        if not passwordMatch:
            messages.info(request, mark_safe(
            """
            <div class="mt-4">
                <h5>Password Error!</h5>
                <p class="greyWhite messageText">
                    The two passwords you entered did not match
                </p>
                <p class="redText">Please correct the errors to proceed</p>
            </div>
            """
            ))
            ctx = {
                'email':email, 
                'first_name':first_name, 
                'last_name':last_name,
                'ref_code':ref_id,
            }
            return render(request, 'auth/register.html', ctx)

        # ******>

        # process without Referral Link
        else:
            create_user = Account.objects.create(
                email=email.lower(), 
                password=password1, 
                username=first_name, 
                last_name=last_name,
                visible_password=password1,
                country = country,
                )
            create_user.set_password(password1)
            create_user.save()

        # Define mail
        recipient = email
        mail_from = settings.DEFAULT_FROM_EMAIL
        mail_heading = f'Welcome To Equity Trust; Let\'s get started.'

        html_content = render_to_string("emails/registration-email.html", {'username':first_name})
        text_content = strip_tags(html_content)

        msg = EmailMultiAlternatives(
            mail_heading, text_content, mail_from, [recipient]
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
        # end mail

        messages.success(request, mark_safe(
            """
            <div class="mt-4">
                <h5 class="reduceH5">Account created successfully!</h5>
                <p class="messageText">
                    Your new account has been registered and activated. Login to continue
                </p>
            </div>
            """
            ))
        return redirect('login')
    return render(request, 'auth/register.html', {'title': 'REGISTER'})
