from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Обязательное поле. Введите действующий email.')
    name1 = forms.CharField(label='Имя', max_length=254)
    name2 = forms.CharField(label='Фамилия', max_length=254)
    name3 = forms.CharField(label='Отчество', max_length=254)
    org = forms.CharField(label='Название организации', max_length=254)
    city = forms.CharField(label='Город', max_length=254)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput, max_length=254)

    class Meta:
        model = User
        fields = ('email', 'name1', 'name2', 'name3', 'org', 'city', 'password')

class LoginForm(AuthenticationForm):
    name1 = forms.CharField(label='Имя', max_length=254)
    name2 = forms.CharField(label='Фамилия', max_length=254)
    name3 = forms.CharField(label='Отчество', max_length=254)
    email = forms.EmailField(label='Электронная почта', max_length=254)
    code = forms.CharField(label='Секретный код', help_text='Получите данный код у организации', max_length=254)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput, max_length=254)
