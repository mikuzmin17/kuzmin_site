# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth import get_user_model
from blog.models import Comment

User = get_user_model()



class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['message'].label = 'Место для Ваших комментариев'

    class Meta:
        model = Comment
        fields = ('message', )

class LoginForm(forms.Form):

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not  User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователя с этим именем не существует!!!')
        user = User.objects.get(username=username)
        if not user.check_password(password):
            raise forms.ValidationError('Пароль неверный!!!')

class RegistrationForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)
    password_check = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'password_check',

        ]
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Авторский псевдоним'
        self.fields['password_check'].label = 'Повторите Ваш пароль'
        self.fields['email'].help_text = 'Обязательное поле'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        password_check = self.cleaned_data['password_check']

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с этим именем уже существует!!!')
        if password != password_check:
            raise forms.ValidationError('Пароль не совпадает!!!')