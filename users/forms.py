from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.contrib.auth import authenticate, get_user_model

custom_user_model = get_user_model()

class UserRegistrationForm(UserCreationForm):
    """
    Форма регистрации пользователя.
    """
    email = forms.EmailField(required=True)


    class Meta:
        model = custom_user_model
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["placeholder"] = field.label or ""
    
    def save(self, commit=True):
        """
        Сохраняет пользователя и связывает его с электронной почтой.
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
        return user
    




class UsernameOrEmailAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="Логин или Email",
        widget=forms.TextInput(attrs={"autofocus": True, "class": "form-control", "placeholder": "Логин или Email"}),
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("Неверный логин/email или пароль.")
            else:
                self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data
    

class CustomProfileUpdateForm(forms.ModelForm):
    """
    Форма для обновления профиля пользователя.
    """
    class Meta:
        model = custom_user_model
        fields = ['first_name', 'last_name', 'avatar', 'birth_date', 'telegaram', 'phone']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'telegaram': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }

    
class CustomPasswordChangeForm(PasswordChangeForm):
    """
    Форма для изменения пароля пользователя.
    """
    old_password = forms.CharField(
        label="Старый пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Старый пароль"}),
    )
    new_password1 = forms.CharField(
        label="Новый пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Новый пароль"}),
    )
    new_password2 = forms.CharField(
        label="Подтверждение нового пароля",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Подтверждение нового пароля"}),
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["placeholder"] = field.label or ""

class CustomPasswordResetForm(PasswordResetForm):
    """
    Форма для сброса пароля пользователя.
    """
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Введите ваш Email"}),
    )


class CustomSetPasswordForm(SetPasswordForm):
    """
    Форма для установки нового пароля после сброса.
    """
    new_password1 = forms.CharField(
        label="Новый пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Новый пароль"}),
    )
    new_password2 = forms.CharField(
        label="Подтверждение нового пароля",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Подтверждение нового пароля"}),
    )

