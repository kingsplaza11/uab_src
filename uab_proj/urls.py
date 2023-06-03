from django.contrib import admin
from django.urls import path, include
from main.views import *
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('core/', include('bank.urls')),
    path('site-admin/', include('site_admin.urls')),
    # ==
    path('', index, name='index'),
    path('terms-and-conditions', terms, name='terms'),
    path('policy', policy, name='policy'),
    path('faqs', faq, name='faqs'),
    path('support', support, name='support'),
    path('about', about, name='about'),
    path('buisnesschecking/', buisnesschecking, name='buisnesschecking'),
    path('buisnessdebitcards/', buisnessdebitcards, name='buisnessdebitcards'),
    path('buisnesssavings/', buisnesssavings, name='buisnesssavings'),
    path('careers/', careers, name='careers'),
    path('checking_accounts/', checking_accounts, name='checking_accounts'),
    path('debitcards/', debitcards, name='debitcards'),
    path('location/', location, name='location'),
    path('non_profit/', non_profit, name='non_profit'),
    path('orderchange/', orderchange, name='orderchange'),
    path('serve/', serve, name='serve'),
    path('savingcds/', savingcds, name='savingcds'),
    path('shareholders/', shareholders, name='shareholders'),
    path('tresurymanagement/', tresurymanagement, name='tresurymanagement'),
    path('services/', services, name='services'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)