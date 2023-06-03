from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('validate-signup-email/', csrf_exempt(views.UserAccountsViews.check_unique_email), name='validate-signup-email'),
    path('signup', views.signup_view, name='signup-view'),
    path('create-account', views.UserAccountsViews.create_user_account, name='create-account'),
    path('login/', views.login_view, name='login-view'),
    path('validate-login-detail', views.validate_login_data, name='validate-login-detail'),
    path('login-user', views.login_user, name='authenticate-user'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('change-password', views.change_password, name='change-password'),
    path('profile', views.user_profile, name='profile'),
    path('set-pin', views.set_transfer_pin, name='set-pin'),
    path('account-security', views.account_security_notice, name='account-security'),
    path('set-photo', views.set_profile_photo, name='set-photo'),


    # forgot password section
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='auth/password_reset.html'), name='password-reset'),

    path('password-reset-done/', auth_views.PasswordResetDoneView.as_view(template_name='auth/password_reset_done.html'), name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='auth/password_reset_confirm.html'), name='password_reset_confirm'),
    
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='auth/password_reset_complete.html'), name='password_reset_complete'),
]
