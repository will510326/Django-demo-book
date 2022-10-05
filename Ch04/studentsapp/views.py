from django.shortcuts import render
from studentsapp.models import student
# Create your views here.


def listone(request):
    try:
        unit = student.objects.get(cName='林木田')
    except:
        errormessage = '(讀取錯誤！！)'
    return render(request, 'listone.html', locals())


def listall(request):
    try:
        units = student.objects.all()
    except:
        errormessage = '(讀取錯誤！！)'
    return render(request, 'listall.html', locals())


def index(request):
    try:
        units = student.objects.all()
    except:
        errormessage = '(讀取錯誤！！)'
    return render(request, 'index.html', locals())
