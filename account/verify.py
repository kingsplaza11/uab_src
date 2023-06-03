import datetime
# from .models import AccountVerification
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required



# ==>
# @login_required
# def account_verification_func(request):
#     user = request.user

#     if request.method == 'POST':
#         email = request.POST['email']
#         date_of_birth = request.POST['date-of-birth']

#         # ==>
#         phone_number = request.POST['phone-number']
#         home_address = request.POST['home-address']
#         # ==>

#         employment_status = request.POST['employment-status']
#         document = request.FILES.get('document')

#         # ==>
        
#         try:
#             object = AccountVerification.objects.get(user=user)
#             object.c_email = email
#             object.phone_number = phone_number
#             object.current_home_address = home_address
#             object.employment_status = employment_status
#             object.date_of_birth = date_of_birth


#             object.document = document
#             object.status = 'waiting'

#             object.save()
        
#         except:
#             # create data Tables
#             AccountVerification.objects.create(
#                 user = user,
#                 c_email = email,
#                 phone_number = phone_number,
#                 current_home_address = home_address,
#                 employment_status = employment_status,
#                 date_of_birth = date_of_birth,

#                 document = document,
#                 status = 'waiting'
#             ).save()

#         messages.success(request, mark_safe(
#             f"""
#                 <h5 class="textColor reduceH5"><b>Data Submitted!</b></h5>
#                 <p class="moreBlack">
#                     Your account verification is in process. You'll be notified accordingly through your email.
#                 </p>
#             """
#             ))
#         return redirect('account-verification')
#     return redirect('account-verification')



