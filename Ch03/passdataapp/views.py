from urllib import request
from django.shortcuts import render
import random
# Create your views here.


def dice(request):
    no = random.randint(1, 6)
    return render(request, 'dice.html', {'no': no})


def dice2(request):
    no1 = random.randint(1, 6)
    no2 = random.randint(1, 6)
    no3 = random.randint(1, 6)
    return render(request, 'dice2.html', locals())


time = 0


def dice3(request):
    global time
    time = time + 1
    local_times = time
    username = 'Wayne'
    dice_no = {'no': random.randint(1, 6)}
    return render(request, 'dice3.html', locals())


def show(request):
    person1 = {'name': 'Wayne', 'phone': 123456789, 'age': 25}
    person2 = {'name': 'Wayne', 'phone': 123456789, 'age': 25}
    person3 = {'name': 'Jack', 'phone': 123456789, 'age': 25}
    persons = [person1, person2, person3]
    return render(request, 'show.html', locals())


def filter(request):
    value = 4
    list1 = [1, 2, 3]
    pw = '芝麻開門'
    html = '<h1> Hello </h1>'
    value2 = False
    return render(request, 'filter.html', locals())
