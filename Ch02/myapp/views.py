from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
# Create your views here.


def sayhello(request):
    return HttpResponse("Hello Django")


def sayhello2(request, username):
    return HttpResponse("Hello " + username)


def sayhello3(request, username):
    now = datetime.now()
    return render(request, 'hello3.html', locals())


def sayhello4(request, username):
    now = datetime.now()
    return render(request, 'hello4.html', locals())
