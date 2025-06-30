from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Service, Order, Review, Master

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
        fields = ['client_name', 'phone', 'master', 'appointment_date', 'services', 'comment']
        widgets = {
            'appointment_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'services': forms.SelectMultiple(attrs={
                'class': 'form-control',
                "id": "id_services",
                }),
            'master': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_master',
                }),
            'client_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Номер телефона'}),
            "comment": forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Комментарий (необязательно)'}),
        }

    def __init__(self, *args, **kwargs):
        master_id = kwargs.pop('master_id', None)
        super().__init__(*args, **kwargs)
        
        if master_id:
            try:
                master = Master.objects.get(id=master_id)
                self.fields['services'].queryset = master.services.all()
            except Master.DoesNotExist:
                self.fields['services'].queryset = Service.objects.none()
        else:
            # Если мастер не выбран, показываем все услуги
            self.fields['services'].queryset = Service.objects.all()

class ReviewForm(forms.ModelForm):
    """
    Форма для создания отзыва.
    """
    class Meta:
        model = Review
        fields = ['master','text', 'client_name', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Напишите отзыв'}),
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'client_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя', 'readonly': True}),
            'master': forms.Select(attrs={'class': 'form-control'}),
        }