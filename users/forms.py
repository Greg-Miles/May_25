from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class UserRegistrationForm(UserCreationForm):
    """
    Форма регистрации пользователя.
    """
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
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
        widget=forms.TextInput(attrs={"autofocus": True})
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