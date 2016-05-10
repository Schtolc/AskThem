from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
from myapp.models import *
from myapp.forms import *
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.http.response import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import SimpleUploadedFile
import json


# Create your views here.

def create_page(data_list, data_on_page, page):
    paginator = Paginator(data_list, data_on_page)
    try:
        page_answers = paginator.page(page)
    except PageNotAnInteger:
        page_answers = paginator.page(1)
    except EmptyPage:
        page_answers = paginator.page(paginator.num_pages)
    return page_answers


def new_questions(request):
    question_list = Question.objects.new()
    return render(request, 'questions.html', {'questions': create_page(question_list, 10, request.GET.get('page')),
                                              'title': 'New questions',
                                              })


def hot_questions(request):
    question_list = Question.objects.hot()
    return render(request, 'questions.html', {'questions': create_page(question_list, 10, request.GET.get('page')),
                                              'title': 'Hot questions',
                                              })


def tags_question(request, tag):
    question_list = Question.objects.by_tags(tag)
    return render(request, 'questions.html', {'questions': create_page(question_list, 10, request.GET.get('page')),
                                              'title': 'Questions with tag: ' + tag,
                                              })


def id_question(request, q_id):
    answers_list = Answer.objects.by_id(q_id)
    question = Question.objects.by_id(q_id)
    if request.method == 'POST':
        if request.user.is_authenticated():
            form = AnswerForm(request.POST)
            if form.is_valid():
                a = Answer.objects.new_answer(form.cleaned_data.get('text'), request.user, question)
                page = Answer.objects.get_page(a.id, 6)
                return HttpResponseRedirect('/question/' + str(int(q_id)) + '?page=' + str(page) + '#a_' + str(a.id))
        else:
            return HttpResponseRedirect('/login?next=/question/' + str(int(q_id)))
    else:
        form = AnswerForm()
    return render(request, 'answers.html', {
        'answers': create_page(answers_list, 6, request.GET.get('page')),
        'question': question,
        'title': "Question# " + str(q_id),
        'form': form,
    })


def signup(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data.get('password') != form.cleaned_data.get('password_again'):
                form.add_error(None, ValidationError(_('Passwords do not match')))

            elif Profile.objects.email_in_use(form.cleaned_data.get('email')):
                form.add_error(None, ValidationError(_('Email already exists')))

            else:
                Profile.objects.new_user(form.cleaned_data.get('username'), form.cleaned_data.get('email'), form.cleaned_data.get('password'),
                                         request.FILES['picture'], )
                user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
                login(request, user)
                return HttpResponseRedirect('/')

    else:
        form = UserRegisterForm()
    return render(request, 'signup.html', {'form': form})


@login_required()
def edit(request, option):
    error = ''
    if request.method == 'POST':

        if option == 'info':
            form = UserChangeInfo(request.POST)
            if form.is_valid():
                if form.cleaned_data.get('email') != request.user.email and Profile.objects.email_in_use(form.cleaned_data.get('email')):
                    error = 'Email already exists'
                else:
                    Profile.objects.change_user(form.cleaned_data.get('username'), form.cleaned_data.get('email'),
                                                request.user.get_username())
                    error = 'Info changed'
            else:
                error = 'All fields is required'

        elif option == 'password':
            form = UserChangePassword(request.POST)
            if form.is_valid():
                if not request.user.check_password(form.cleaned_data.get('old_password')):
                    error = 'Invalid password'
                elif form.cleaned_data.get('new_password') != form.cleaned_data.get('password_again'):
                    error = 'Passwords do not match'
                else:
                    Profile.objects.change_password(form.cleaned_data.get('new_password'), request.user.get_username())
                    error = 'Password changed'
            else:
                error = 'All fields is required'

        elif option == 'picture':
            form = UserChangePicture(request.POST, request.FILES)
            if form.is_valid():
                Profile.objects.change_pic(request.user.get_username(), request.FILES['picture'])
                error = 'Picture changed'
            else:
                error = 'All fields is required '

    # p = Profile.objects.by_username(request.user.get_username())
    data = {'username': request.user.username,
            'email': request.user.email,
            }
    form_info = UserChangeInfo(data)
    form_password = UserChangePassword()
    form_picture = UserChangePicture
    if error != '':
        form_info.add_error(None, ValidationError(_(error)))
    return render(request, 'settings.html', {'form_info': form_info,
                                             'form_password': form_password,
                                             'form_picture': form_picture})


def login_page(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(request.GET.get('next', '/'))
            else:
                form.add_error(None, ValidationError(_('Wrong login or password')))
    else:
        form = UserLoginForm()

    return render(request, 'login.html', {'form': form,
                                          'next': request.GET.get('next', '/')})


def logout_page(request):
    logout(request)
    redirect_to = request.GET.get('next', '/')
    return HttpResponseRedirect(redirect_to)


@login_required()
def ask(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            q = Question.objects.new_question(form.cleaned_data.get('title'), form.cleaned_data.get('text'), request.user,
                                              form.cleaned_data.get('tags'))
            return HttpResponseRedirect('/question/' + str(q.id))

    else:
        form = QuestionForm()

    return render(request, 'ask.html', {'form': form})


def profile(request, username):
    u = Profile.objects.by_username(username)
    questions = Question.objects.by_username(username)
    answers = Answer.objects.by_username(username)
    return render(request, 'profile.html', {
        'profile': u,
        'questions': questions,
        'answers': answers
    })


@login_required()
def correct(request):
    a = Answer.objects.get(id=request.POST['aid'])
    is_correct = request.POST['checked'] == 'true'
    a.is_correct = is_correct
    a.save()
    return HttpResponse(
        json.dumps({"aid": request.POST['aid'], 'correct': is_correct}),
        content_type="application/json"
    )


@login_required()
def like(request):
    q = Question.objects.get(id=request.POST['qid'])
    u = request.user
    is_like = request.POST['typ'] == 'like'
    l = Like.objects.filter(user=u).filter(question=q)
    if len(l) == 0:
        vote = Like(user=u, question=q, is_like=is_like)
        vote.save()
    else:
        l[0].is_like = is_like
        l[0].save()
    return HttpResponse(
        json.dumps({"qid": request.POST['qid'], 'like': is_like}),
        content_type="application/json"
    )
