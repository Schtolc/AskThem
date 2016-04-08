from django.shortcuts import render
from django.http import HttpResponse
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
    return render(request, 'questions.html',
                  {'questions': questions[:10],
                   'title': 'New questions',
                   })


def hot_questions(request):
    tmp_questions = sorted(questions, key=lambda k: k['likes'], reverse=True)
    return render(request, 'questions.html',
                  {'questions': tmp_questions[:10],
                   'title': 'Hot questions',
                   })


def tags_question(request, tag):
    tmp_questions = []
    for question in questions:
        if tag in question['tags']:
            tmp_questions.append(question)
    return render(request, 'questions.html', {
        'questions': tmp_questions,
        'title': 'Questions with tag: ' + tag,
    })


def id_question(request, id):
    return render(request, 'answers.html', {
        'answers': answers,
        'question': questions[next(index for (index, d) in enumerate(questions) if str(d["id"]) == str(id))],
        'title': "Question# " + str(id),
    })


def signup(request):
    return render(request, 'signup.html')


def login(request):
    return render(request, 'login.html')


def ask(request):
    return render(request, 'ask.html')
