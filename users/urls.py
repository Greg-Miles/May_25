from django.urls import path
from .views import register, user_login, user_logout, UserCancelOrderView, ProfileView

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/delete_order/<int:pk>/', UserCancelOrderView.as_view(), name='cancel_order'),
]
