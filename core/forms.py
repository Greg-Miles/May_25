from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Service, Order, Review

class UserRegistrationForm(UserCreationForm):
    """
    Форма регистрации пользователя.
    """
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        """
        Сохраняет пользователя и связывает его с электронной почтой.
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
        return user


class OrderForm(forms.ModelForm):
    """
    Форма для создания заказа.
    """
    class Meta:
        model = Order
        fields = ['client_name', 'phone', 'master', 'appointment_date', 'services']
        widgets = {
            'appointment_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'services': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'master': forms.Select(attrs={'class': 'form-control'}),
        }

class ReviewForm(forms.ModelForm):
    """
    Форма для создания отзыва.
    """
    class Meta:
        model = Review
        fields = ['text', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Напишите отзыв'}),
            'rating': forms.Select(attrs={'class': 'form-control'}),
        }