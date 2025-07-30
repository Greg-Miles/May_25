from django.urls import path
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
]
