from django.contrib.auth.models import User
from django import forms


class UserLoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput())


class UserRegisterForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', max_length=100, widget=forms.EmailInput(
        attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_again = forms.CharField(label='Repeat password', max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    # pic = forms.CharField(label='Pic', max_length=100)
    picture = forms.ImageField(label='Picture', widget=forms.FileInput())

    # def clean_password


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


class UserChangePicture(forms.Form):
    picture = forms.ImageField(label='Picture')
