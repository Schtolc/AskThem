from django.contrib.auth.models import User
from django import forms


class UserLoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput())


class UserRegisterForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    email = forms.EmailField(label='Email', max_length=100)
    password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput())
    password_again = forms.CharField(label='Repeat password', max_length=100, widget=forms.PasswordInput())
    # pic = forms.CharField(label='Pic', max_length=100)
    picture = forms.ImageField(label='Picture')


class QuestionForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100)
    text = forms.CharField(label='Text', max_length=1000, widget=forms.Textarea)
    tags = forms.CharField(label='Tags', max_length=100)


class AnswerForm(forms.Form):
    text = forms.CharField(label='Text', max_length=1000, widget=forms.Textarea)


class UserChangeInfo(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    email = forms.EmailField(label='Email', max_length=100)


class UserChangePassword(forms.Form):
    old_password = forms.CharField(label='Previous password', max_length=100, widget=forms.PasswordInput())
    new_password = forms.CharField(label='New password', max_length=100, widget=forms.PasswordInput())
    password_again = forms.CharField(label='Repeat password', max_length=100, widget=forms.PasswordInput())
