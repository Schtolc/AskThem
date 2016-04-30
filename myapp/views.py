from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
from myapp.models import *
from myapp.forms import *
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.http.response import HttpResponseRedirect
from django.contrib.auth.decorators import login_required


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
                a = Answer(text=request.POST['text'], author=request.user, question=question)
                a.save()
                return HttpResponseRedirect('/question/' + str(int(q_id)))
        else:
            return HttpResponseRedirect('/login?next=/question/' + str(int(q_id)))
    else:
        form = AnswerForm()
    return render(request, 'answers.html', {
        'answers': create_page(answers_list, 3, request.GET.get('page')),
        'question': question,
        'title': "Question# " + str(q_id),
        'form': form,
    })


def signup(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            if request.POST['password'] != request.POST['password_again']:
                form.add_error(None, ValidationError(_('Passwords do not match')))

            elif len(User.objects.all().filter(email=request.POST['email'])) != 0:
                form.add_error(None, ValidationError(_('Email already exists')))

            else:
                u = User.objects.create_user(username=request.POST['username'], email=request.POST['email'],
                                             password=request.POST['password'])
                u.save()
                p = Profile(avatar=u, pic=request.POST['pic'])
                p.save()
                return HttpResponseRedirect('/')

    else:
        form = UserRegisterForm()
    return render(request, 'signup.html', {'form': form})


def login_page(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(request.POST.get('next', '/'))
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
            q = Question(title=request.POST['title'], text=request.POST['text'], author=request.user)
            q.save()
            for tag in request.POST['tags'].replace(' ', '').split(','):
                t = Tag.objects.all().filter(title=tag).first()
                if not t:
                    t = Tag(title=tag)
                    t.save()
                q.tags.add(t)
                q.save()
            return HttpResponseRedirect('/question/' + str(int(q.id)))

    else:
        form = QuestionForm()

    return render(request, 'ask.html', {'form': form})
