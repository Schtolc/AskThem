from django.contrib.auth.models import User
from myapp.models import *
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

    def save(self):
        u = User.objects.create_user(username=self.cleaned_data['username'], email=self.cleaned_data['email'],
                                     password=self.cleaned_data['password'])
        u.save()
        p = Profile(avatar=u, picture=self.cleaned_data['picture'])
        p.save()


class QuestionForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    text = forms.CharField(label='Text', max_length=1000, widget=forms.Textarea(attrs={'class': 'form-control'}))
    tags = forms.CharField(label='Tags', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))

    def save(self, request):
        q = Question(title=self.cleaned_data['title'], text=self.cleaned_data['text'], author=request.user)
        q.save()
        for tag in self.cleaned_data['tags'].replace(' ', '').split(','):
            t = Tag.objects.all().filter(title=tag).first()
            if not t:
                t = Tag(title=tag)
                t.save()
            q.tags.add(t)
            q.save()
        return q.id


class AnswerForm(forms.Form):
    text = forms.CharField(label='Text', max_length=1000, widget=forms.Textarea(attrs={'class': 'form-control'}))

    def save(self, request, question):
        a = Answer.objects.new_answer(self.cleaned_data.get('text'), request.user, question)
        page = Answer.objects.get_page(a.id, 6)
        return (a.id, page)


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

    def save(self):
        u = User.objects.get(username=self.request.user.username)
        u.username = self.cleaned_data['username']
        u.email = self.cleaned_data['email']
        u.save()


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

    def save(self):
        u = User.objects.get(username=self.request.user.username)
        u.set_password(self.cleaned_data['new_password'])
        u.save()


class UserChangePicture(forms.Form):
    picture = forms.ImageField(label='Picture', widget=forms.FileInput())

    def save(self, request):
        p = Profile.objects.by_username(request.user.username)
        p.picture = self.cleaned_data['picture']
        p.save()
