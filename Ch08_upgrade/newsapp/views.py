from cgitb import enable
from re import sub
from unicodedata import category
from django.shortcuts import render, redirect
from newsapp import models
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.csrf import ensure_csrf_cookie
from django import template
import math
# Create your views here.

page1 = 1  # 目前頁面


def index(request, pageindex=None):
    global page1  # 重複開啟本網頁時需要保留 page1 的值
    pagesize = 8  # 每頁顯示的資料筆數
    newsall = models.NewsUnit.objects.all().order_by('id')  # 讀取新聞資料表，依時間遞減排序
    datasize = len(newsall)  # 新聞筆數
    totpage = math.ceil(datasize / pagesize)  # 總頁數
    if pageindex == None:  # 無參數
        page1 = 1
        newsunits = models.NewsUnit.objects.filter(
            enable=True).order_by('id')[:pagesize]
    elif pageindex == '1':  # 上一頁
        start = (page1-2)*pagesize  # 該頁第一筆資料
        if start >= 0:
            newsunits = models.NewsUnit.objects.filter(
                enable=True).order_by('-id')[start: start+pagesize]
            page1 -= 1
    elif pageindex == '2':  # 下一頁
        start = page1 * pagesize  # 該頁第一筆資料
        if start < datasize:  # 有下頁資料就顯示
            newsunits = models.NewsUnit.objects.filter(
                enable=True).order_by('-id')[start:(start+pagesize)]
            page1 += 1
    elif pageindex == '3':  # 由詳細頁面返回首頁
        start = (page1 - 1) * pagesize  # 取得原有頁面第１筆資料
        newsunits = models.NewsUnit.objects.filter(
            enable=True).order_by('-id')[start: (start + pagesize)]
    currentpage = page1  # 將目前頁面以區域變數傳回html
    return render(request, 'index.html', locals())


def detail(request, detailid=None):
    unit = models.NewsUnit.objects.get(id=detailid)  # 根據參數取得資料
    category = unit.catego
    title = unit.title
    pubtime = unit.pubtime
    nickname = unit.nickname
    message = unit.message
    unit.press += 1  # 點閱數加1
    unit.save()  # 儲存資料
    return render(request, 'detail.html', locals())


def login(request):  # 登入
    messages = ''
    if request.method == 'POST':
        name = request.POST['username'].strip()
        password = request.POST['password']
        user1 = authenticate(username=name, password=password)  # 驗證
        if user1 is not None:
            if user1.is_active:  # 帳號有效的話
                auth.login(request, user1)
                return redirect('/adminmain/')  # 開啟管理介面
            else:
                messages = '帳號未啟用'
        else:
            messages = '登入失敗'
    return render(request, 'login.html', locals())


def logout(request):
    auth.logout(request)
    return redirect('/index/')


def adminmain(request, pageindex=None):
    global page1
    pagesize = 8
    newsall = models.NewsUnit.objects.all().order_by('-id')
    datasize = len(newsall)
    totpage = math.ceil(datasize / pagesize)
    if pageindex == None:
        page1 = 1
        newsunits = models.NewsUnit.objects.order_by('-id')[:pagesize]
    elif pageindex == '1':
        start = (page1-2)*pagesize
        if start >= 0:
            newsunits = models.NewsUnit.objects.order_by(
                '-id')[start:(start+pagesize)]
            page1 -= 1
    elif pageindex == '2':
        start = page1*pagesize
        if start < datasize:
            newsunits = models.NewsUnit.objects.order_by(
                '-id')[start:(start+pagesize)]
            page1 += 1
    elif pageindex == '3':
        start = (page1-1)*pagesize
        newsunits = models.NewsUnit.objects.order_by(
            '-id')[start:(start+pagesize)]
    currentpage = page1
    return render(request, "adminmain.html", locals())


def newsadd(request):
    message = ''
    category = request.POST.get('news_type', '')  # 取得輸入類別
    subject = request.POST.get('news_subject', '')
    editor = request.POST.get('news_editor', '')
    content = request.POST.get('news_content', '')
    ok = request.POST.get('news_ok', '')
    if subject == '' or editor == '' or content == '':  # 若有欄位未填就顯示訊息
        message = '每一個欄位都要填寫'
    else:
        if ok == 'yes':
            enable = True
        else:
            enable = False
        unit = models.NewsUnit.objects.create(
            catego=category, nickname=editor, title=subject, message=content, enable=enable, press=0)
        unit.save()
        return redirect('/adminmain/')
    return render(request, 'newsadd.html', locals())


def newsedit(request, newsid=None, edittype=None):  # 修改資料
    unit = models.NewsUnit.objects.get(id=newsid)  # 讀取選定資料
    categories = ['公告', '更新', '活動', '其他']
    if edittype == None:  # 進入修改頁面，顯示原有資料
        type = unit.catego
        subject = unit.title
        editor = unit.nickname
        content = unit.message
        ok = unit.enable
    elif edittype == '1':  # 修改完畢，存檔
        category = request.POST.get('news_type', '')  # 取得輸入類別
        subject = request.POST.get('news_subject', '')
        editor = request.POST.get('news_editor', '')
        content = request.POST.get('news_content', '')
        ok = request.POST.get('news_ok', '')
        if ok == 'yes':
            enable = True
        else:
            enable = False
        unit.catego = category
        unit.nickname = editor
        unit.title = subject
        unit.message = content
        unit.enable = enable
        unit.save()
        return redirect('/adminmain/')
    return render(request, 'newsedit.html', locals())


def newsdelete(request, newsid=None, deletetype=None):  # 刪除資料
    unit = models.NewsUnit.objects.get(id=newsid)
    if deletetype == None:  # 進入刪除頁面，顯示原有資料
        type = str(unit.catego.strip())
        subject = unit.title
        editor = unit.nickname
        content = unit.message
        date = unit.pubtime
    elif deletetype == '1':  # 按刪除鈕
        unit.delete()
        return redirect('/adminmain/')
    return render(request, 'newsdelete.html', locals())
