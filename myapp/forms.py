from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError


class UserLoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', max_length=100,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserRegisterForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', max_length=100, widget=forms.EmailInput(
        attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', max_length=100,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_again = forms.CharField(label='Repeat password', max_length=100,
                                     widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    picture = forms.ImageField(label='Picture', widget=forms.FileInput())

    def clean_email(self):
        data = self.cleaned_data['email']
        if len(User.objects.all().filter(email=data)) != 0:
            raise forms.ValidationError('Email in Use')
        else:
            return data

    def clean_password_again(self):
        password_once = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password_once != password_again:
            raise forms.ValidationError('Passwords do not match')
        else:
            return password_again


class QuestionForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    text = forms.CharField(label='Text', max_length=1000, widget=forms.Textarea(attrs={'class': 'form-control'}))
    tags = forms.CharField(label='Tags', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))


class AnswerForm(forms.Form):
    text = forms.CharField(label='Text', max_length=1000, widget=forms.Textarea(attrs={'class': 'form-control'}))


class UserChangeInfo(forms.Form):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(UserChangeInfo, self).__init__(*args, **kwargs)

    username = forms.CharField(label='Username', max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        data = self.cleaned_data['email']
        if len(User.objects.all().filter(email=data)) != 0 and data != self.request.user.email:
            raise forms.ValidationError('Email in Use')
        else:
            return data


class UserChangePassword(forms.Form):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(UserChangePassword, self).__init__(*args, **kwargs)

    old_password = forms.CharField(label='Previous password', max_length=100,
                                   widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password = forms.CharField(label='New password', max_length=100,
                                   widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_again = forms.CharField(label='Repeat password', max_length=100,
                                     widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_old_password(self):
        data = self.cleaned_data['old_password']
        if not self.request.user.check_password(data):
            raise forms.ValidationError('Invalid password')
        else:
            return data

    def clean_password_again(self):
        password_once = self.cleaned_data['new_password']
        password_again = self.cleaned_data['password_again']
        if password_once != password_again:
            raise forms.ValidationError('Passwords do not match')
        else:
            return password_again


class UserChangePicture(forms.Form):
    picture = forms.ImageField(label='Picture', widget=forms.FileInput())
