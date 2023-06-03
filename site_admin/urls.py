from django.urls import path
from . import views

urlpatterns = [
    path('', views.users, name='users'),
    path('user-account-detail/<int:pk>/', views.user_detail, name='user-detail'),
    path('fund-account/<int:pk>/', views.fund_account, name='fund-account'),
    path('create-logs', views.create_logs_view, name='create-logs-view'),
    path('create-logs-func', views.create_logs, name='create-logs-func'),
    path('impose-restriction', views.impose_restrictions, name='impose-restriction'),
    path('add-bank', views.add_bank, name='add-bank'),
    path('create-account-admin', views.create_account_admin, name='create-account-admin'),
    path('banks-created', views.banks_created, name='banks-created'),

    path('deleteUserAccount/<int:id>', views.delete_account, name="delete-account"),
    path('support-messages', views.support_message, name="support-messages"),
    path('close-ticket/<int:id>', views.close_support_request, name="close-ticket"),
    path('send-mail', views.send_mails, name="send-mail"),
]