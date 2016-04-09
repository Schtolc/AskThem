from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import random

# Create your views here.

questions = []
answers = []
question_tags = ['give', 'me', 'my', 'flowers', 'while', 'i', 'still', 'can', 'smell', 'them']

for i in range(100):
    questions.append(
        {'id': i,
         'title': 'Question #{}. Some text following question number'.format(i),
         'body': '''Lorem ipsum dolor sit amet, adipiscing elit. Aliquam aliquet pellentesque massa et
                   placerat.  Mauris sed nunc fringilla, faucibus tortor ac, ultrices justo. Proin id semper elit,
                   eu efficitur libero.''',
         'tags': [question_tags[random.randint(0, len(question_tags) - 1)],
                  question_tags[random.randint(0, len(question_tags) - 1)],
                  question_tags[random.randint(0, len(question_tags) - 1)]],
         'likes': random.randint(0, 1000),
         }
    )

for i in range(10):
    answers.append(
        {'id': i,
         'body': '''Lorem ipsum dolor sit amet, adipiscing elit. Aliquam aliquet pellentesque massa et
                   placerat.  Mauris sed nunc fringilla, faucibus tortor ac, ultrices justo. Proin id semper elit,
                   eu efficitur libero.''',
         'likes': random.randint(0, 1000),
         }
    )


def new_questions(request):
    question_list = questions
    paginator = Paginator(question_list, 10)
    page = request.GET.get('page')
    try:
        page_questions = paginator.page(page)
    except PageNotAnInteger:
        page_questions = paginator.page(1)
    except EmptyPage:
        page_questions = paginator.page(paginator.num_pages)

    return render(request, 'questions.html', {'questions': page_questions,
                                              'title': 'New questions',
                                              })


def hot_questions(request):
    question_list = sorted(questions, key=lambda k: k['likes'], reverse=True)
    paginator = Paginator(question_list, 10)
    page = request.GET.get('page')
    try:
        page_questions = paginator.page(page)
    except PageNotAnInteger:
        page_questions = paginator.page(1)
    except EmptyPage:
        page_questions = paginator.page(paginator.num_pages)

    return render(request, 'questions.html', {'questions': page_questions,
                                              'title': 'Hot questions',
                                              })


def tags_question(request, tag):
    tmp_questions = []
    for question in questions:
        if tag in question['tags']:
            tmp_questions.append(question)
    question_list = tmp_questions
    paginator = Paginator(question_list, 10)
    page = request.GET.get('page')
    try:
        page_questions = paginator.page(page)
    except PageNotAnInteger:
        page_questions = paginator.page(1)
    except EmptyPage:
        page_questions = paginator.page(paginator.num_pages)

    return render(request, 'questions.html', {'questions': page_questions,
                                              'title': 'Questions with tag: ' + tag,
                                              })


def id_question(request, id):
    answers_list = answers
    paginator = Paginator(answers_list, 3)
    page = request.GET.get('page')
    try:
        page_answers = paginator.page(page)
    except PageNotAnInteger:
        page_answers = paginator.page(1)
    except EmptyPage:
        page_answers = paginator.page(paginator.num_pages)

    return render(request, 'answers.html', {
        'answers': page_answers,
        'question': questions[next(index for (index, d) in enumerate(questions) if str(d["id"]) == str(id))],
        'title': "Question# " + str(id),
    })


def signup(request):
    return render(request, 'signup.html')


def login(request):
    return render(request, 'login.html')


def ask(request):
    return render(request, 'ask.html')
