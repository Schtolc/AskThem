from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from myapp.models import *
import random


# Create your views here.

def create_page(paginator, page):
    try:
        page_answers = paginator.page(page)
    except PageNotAnInteger:
        page_answers = paginator.page(1)
    except EmptyPage:
        page_answers = paginator.page(paginator.num_pages)
    return page_answers


def new_questions(request):
    question_list = Question.manager.new()
    paginator = Paginator(question_list, 10)
    return render(request, 'questions.html', {'questions': create_page(paginator, request.GET.get('page')),
                                              'title': 'New questions',
                                              })


def hot_questions(request):
    question_list = Question.manager.hot()
    paginator = Paginator(question_list, 10)
    return render(request, 'questions.html', {'questions': create_page(paginator, request.GET.get('page')),
                                              'title': 'Hot questions',
                                              })


def tags_question(request, tag):
    question_list = Question.manager.by_tags(tag)
    paginator = Paginator(question_list, 10)
    return render(request, 'questions.html', {'questions': create_page(paginator, request.GET.get('page')),
                                              'title': 'Questions with tag: ' + tag,
                                              })


def id_question(request, q_id):
    answers_list = Answer.manager.by_id(q_id)
    question = Question.manager.by_id(q_id)
    paginator = Paginator(answers_list, 3)
    return render(request, 'answers.html', {
        'answers': create_page(paginator, request.GET.get('page')),
        'question': question,
        'title': "Question# " + str(q_id),
    })


def signup(request):
    return render(request, 'signup.html')


def login(request):
    return render(request, 'login.html')


def ask(request):
    return render(request, 'ask.html')
