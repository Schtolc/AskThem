from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def hello(request):
    answer = '<h1>Hello World!</h1><h2>'+ request.method +' REQUEST:</h2>'
    if request.method == 'GET':
        d = request.GET
    elif request.method == 'POST':
        d = request.POST
    for key in sorted(d.keys()):
        answer+= '<p>' + key + ' : ' + str(d.get(key)) + '</p>'
    return HttpResponse(answer)
