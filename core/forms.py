from django import forms
from .models import Service, Order, Review, Master




class OrderForm(forms.ModelForm):
    """
    Форма для создания заказа.
    """
    class Meta:
        model = Order
        fields = ['client_name', 'phone', 'master', 'appointment_date', 'services', 'comment',]
        widgets = {
            'appointment_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M',
                ),
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
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        is_staff = kwargs.pop('is_staff', False)
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
    
    def clean(self):
        """
        Проверяет, что услуги и мастер соответствуют друг другу.
        """
        cleaned_data = super().clean()
        services = cleaned_data.get('services')
        master = cleaned_data.get('master')

        if services and master:
            master_services = set(master.services.all())
            selected_services = set(services)
            
            unavailable_services = selected_services - master_services
            if unavailable_services:
                service_names = ', '.join([service.name for service in unavailable_services])
                raise forms.ValidationError(
                    f'Мастер {master.name} не предоставляет следующие услуги: {service_names}'
                )
        return cleaned_data

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