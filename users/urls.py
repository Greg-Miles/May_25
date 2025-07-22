from django.urls import path
from .views import UserLoginView, UserLogoutView, UserCancelOrderView, ProfileView, RegistrationView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/delete_order/<int:pk>/', UserCancelOrderView.as_view(), name='cancel_order'),
]
