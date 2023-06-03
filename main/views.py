from django.shortcuts import render, redirect
from site_admin.models import Support
from utils.unique_generators import GenerateUUIDCode
from django.contrib import messages


def index(request):
    return render(request, 'pages/index.html')


def terms(request):
    return render(request, 'pages/terms.html')


def policy(request):
    return render(request, 'pages/policy.html')


def about(request):
    return render(request, 'pages/about.html')

def diversity(request):
    return render(request, 'pages/diversity.html')


def faq(request):
    return render(request, 'pages/faqs.html')


def blog_1(request):
    return render(request, 'pages/blog-1.html')


def services(request):
    return render(request, "pages/serve.html")


def privacy(request):
    return render(request, "pages/privacy.html")


def bank(request):
    return render(request, "pages/bank.html")


def buisnesschecking(request):
    return render(request, "pages/buisnesschecking.html")


def buisnessdebitcards(request):
    return render(request, "pages/buisnessdebitcards.html")


def careers(request):
    return render(request, "pages/careers.html")


def buisnesssavings(request):
    return render(request, "pages/buisnesssavings.html")


def checking_accounts(request):
    return render(request, "pages/checking-accounts.html")


def debitcards(request):
    return render(request, "pages/debitcards.html")


def location(request):
    return render(request, "pages/location.html")


def non_profit(request):
    return render(request, "pages/non-profit.html")


def orderchange(request):
    return render(request, "pages/orderchange.html")


def serve(request):
    return render(request, "pages/rates.html")


def savingcds(request):
    return render(request, "pages/savingcds.html")


def shareholders(request):
    return render(request, "pages/shareholders.html")


def tresurymanagement(request):
    return render(request, "pages/tresurymanagement.html")


def about(request):
    return render(request, "pages/about.html")


def support(request):
    if request.method == 'POST':
        topic = request.POST.get('topic')
        fullname = request.POST.get('fullname')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        Support.objects.create(
            fullname=fullname, mobile=mobile, email=email, subject=subject,
            message=message, topic=topic, ticket_id = GenerateUUIDCode.alpha_numeric_uid(12)
        )
        messages.success( request, 'Request sent! You will receive an email from us shortly')
        return redirect('support')
    return render(request, 'pages/help.html')