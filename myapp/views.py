from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
from myapp.forms import *
from django.core.exceptions import ValidationError
from django.http.response import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
import json


#
# utility functions
#
def create_page(data_list, data_on_page, page):
    paginator = Paginator(data_list, data_on_page)
    try:
        page_answers = paginator.page(page)
    except PageNotAnInteger:
        page_answers = paginator.page(1)
    except EmptyPage:
        page_answers = paginator.page(paginator.num_pages)
    return page_answers


#
# simple render views
#
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


def profile(request, username):
    u = Profile.objects.by_username(username)
    questions = Question.objects.by_username(username)
    answers = Answer.objects.by_username(username)
    return render(request, 'profile.html', {
        'profile': u,
        'questions': questions,
        'answers': answers
    })


#
# forms views
#
def signup(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
            login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = UserRegisterForm()
    return render(request, 'signup.html', {'form': form})


def login_page(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(request.GET.get('next', '/'))
            else:
                form.add_error(None, ValidationError('Wrong login or password'))
    else:
        form = UserLoginForm()

    return render(request, 'login.html', {'form': form, 'next': request.GET.get('next', '/')})


@login_required()
def logout_page(request):
    logout(request)
    return HttpResponseRedirect(request.GET.get('next', '/'))


@login_required()
def ask(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            qid = form.save(request=request)
            return HttpResponseRedirect('/question/' + str(qid))
    else:
        form = QuestionForm()
    return render(request, 'ask.html', {'form': form})


def id_question(request, q_id):
    answers_list = Answer.objects.by_id(q_id)
    question = Question.objects.by_id(q_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            (aid, page) = form.save(request=request, question=question)
            return HttpResponseRedirect('/question/' + str(q_id) + '?page=' + str(page) + '#a_' + str(aid))
    else:
        form = AnswerForm()
    return render(request, 'answers.html', {
        'answers': create_page(answers_list, 6, request.GET.get('page')),
        'question': question,
        'title': "Question# " + str(q_id),
        'form': form,
    })


@login_required()
def change_info(request):
    if request.method == 'POST':
        form = UserChangeInfo(request.POST, request=request)
        if form.is_valid():
            form.save()
    else:
        form = UserChangeInfo(request=request)

    return render(request, 'settings.html', {'form_info': form, 'form_password': UserChangePassword(),
                                             'form_picture': UserChangePicture()})


@login_required()
def change_password(request):
    if request.method == 'POST':
        form = UserChangePassword(request.POST, request=request)
        if form.is_valid():
            form.save()
    else:
        form = UserChangePassword()

    form_info = UserChangeInfo({'username': request.user.username,
                                'email': request.user.email,}, request=request)
    return render(request, 'settings.html', {'form_info': form_info, 'form_password': form,
                                             'form_picture': UserChangePicture()})


@login_required()
def change_pic(request):
    if request.method == 'POST':
        form = UserChangePicture(request.POST, request.FILES)
        if form.is_valid():
            form.save(request=request)
    else:
        form = UserChangePicture()

    form_info = UserChangeInfo({'username': request.user.username,
                                'email': request.user.email,},
                               request=request)
    return render(request, 'settings.html', {'form_info': form_info, 'form_password': UserChangePassword(),
                                             'form_picture': form})


#
# ajax views
#
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
