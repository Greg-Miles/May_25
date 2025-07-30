from django.urls import path
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.forms import PasswordChangeForm
from .views import (
    CustomLoginView, 
    LogoutConfirmView, 
    CustomLogoutView, 
    UserCancelOrderView, 
    ProfileView, 
    RegistrationView
)


urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout_confirm/', LogoutConfirmView.as_view(), name='logout_confirm'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/delete_order/<int:pk>/', UserCancelOrderView.as_view(), name='cancel_order'),
    path('password_change/', 
        PasswordChangeView.as_view(
            template_name='password_change.html',
            form_class=PasswordChangeForm,
            success_url='done/'),
        name='password_change'),
    path(
        'password_change/done/',
        PasswordChangeDoneView.as_view(template_name='password_change_done.html'),
        name='password_change_done'
        ),
]
