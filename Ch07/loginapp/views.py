from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib import auth
from django.http import HttpResponse
from django.contrib.auth.models import User
# Create your views here.


def adduser(request):
    try:
        user = User.objects.get(username='test')
    except:
        user = None
    if user != None:
        message = user.username + '帳號已建立！'
        return HttpResponse(message)
    else:
        user = User.objects.create_user('test', 'test@test.com', '1234567*')
        user.first_name = 'wen'
        user.last_name = 'lin'
        user.is_staff = True
        user.save()
        return redirect('/admin/')


def index(request):
    if request.user.is_authenticated:
        name = request.user.username
    return render(request, "index.html", locals())


def login(request):
    if request.method == 'POST':
        name = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=name, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                message = '登入成功'
                return redirect('/index/')
            else:
                message = '沒有這帳號'
        else:
            message = '登入失敗'
    return render(request, 'login.html', locals())


def logout(request):
    auth.logout(request)
    return redirect('/index/')
