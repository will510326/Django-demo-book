from django.shortcuts import render, redirect
from albumapp import models
from django.contrib.auth import authenticate
from django.contrib import auth
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

def index(request):
	albums = models.AlbumModel.objects.all().order_by('-id')  #讀取所有相簿
	totalalbum = len(albums)  #相簿總數
	photos = []  #每一相簿第1張相片串列
	lengths = []  #每一相簿的相片總數串列
	for album in albums:
		photo = models.PhotoModel.objects.filter(palbum__atitle=album.atitle).order_by('-id')  #讀取相片
		lengths.append(len(photo))  #加入相片總數
		if len(photo) == 0:  #若無相片加入空字串
			photos.append('')
		else:
			photos.append(photo[0].purl)  #加入第1張相片
	return render(request, "index.html", locals())
	
def albumshow(request, albumid=None):  #顯示相簿
	album = albumid  #以區域變數傳送給html
	photos = models.PhotoModel.objects.filter(palbum__id=album).order_by('-id')  #讀取所有相片
	monophoto = photos[0]  #第1張相片
	totalphoto = len(photos)  #相片總數
	return render(request, "albumshow.html", locals())
	
def albumphoto(request, photoid=None, albumid=None):  #顯示單張相片
	album = albumid  #以區域變數傳送給html
	photo = models.PhotoModel.objects.get(id=photoid)  #取得點選的相片
	photo.phit += 1  #點擊數加1
	photo.save()  #儲存資料
	return render(request, "albumphoto.html", locals())

def login(request):  #登入
	messages = ''  #初始時清除訊息
	if request.method == 'POST':  #如果是以POST方式才處理
		name = request.POST['username'].strip()  #取得輸入帳號
		password = request.POST['passwd']  #取得輸入密碼
		user1 = authenticate(username=name, password=password)  #驗證
		if user1 is not None:  #驗證通過
			if user1.is_active:  #帳號有效
				auth.login(request, user1)  #登入
				return redirect('/adminmain/')  #開啟管理頁面
			else:  #帳號無效
				message = '帳號尚未啟用！'
		else:  #驗證未通過
			message = '登入失敗！'
	return render(request, "login.html", locals())

def logout(request):  #登出
	auth.logout(request)
	return redirect('/index/')

def adminmain(request, albumid=None):  #管理頁面
	if albumid == None:  #按相簿管理鈕進管理頁面
		albums = models.AlbumModel.objects.all().order_by('-id')
		totalalbum = len(albums)
		photos = []
		lengths = []
		for album in albums:
			photo = models.PhotoModel.objects.filter(palbum__atitle=album.atitle).order_by('-id')
			lengths.append(len(photo))
			if len(photo) == 0:
				photos.append('')
			else:
				photos.append(photo[0].purl)
	else:  #按刪除相簿鈕
		album = models.AlbumModel.objects.get(id=albumid)  #取得相簿
		photo = models.PhotoModel.objects.filter(palbum__atitle=album.atitle).order_by('-id')  #取得所有相片
		for photounit in photo:  #刪除所有相片檔案
			os.remove(os.path.join(settings.MEDIA_ROOT, photounit.purl ))
		album.delete()  #移除相簿
		return redirect('/adminmain/')
	return render(request, "adminmain.html", locals())

def adminadd(request):  #新增相簿
	message = ''
	title = request.POST.get('album_title', '')  #取得輸入資料
	location = request.POST.get('album_location', '')
	desc = request.POST.get('album_desc', '')
	if title=='':  #按新增相簿鈕進入此頁
		message = '相簿名稱一定要填寫...'
	else:  #按確定新增鈕
		unit = models.AlbumModel.objects.create(atitle=title, alocation=location, adesc=desc)
		unit.save()
		return redirect('/adminmain/')
	return render(request, "adminadd.html", locals())

def adminfix(request, albumid=None, photoid=None, deletetype=None):  #相簿維護
    album = models.AlbumModel.objects.get(id=albumid)  #取得指定相簿
    photos = models.PhotoModel.objects.filter(palbum__id=albumid).order_by('-id')
    totalphoto = len(photos)
    if photoid != None:  #不是由管理頁面進入本頁面
        if photoid == 999999:  #按更新及上傳資料鈕
            album.atitle = request.POST.get('album_title', '')  #更新相簿資料
            album.alocation = request.POST.get('album_location', '')
            album.adesc = request.POST.get('album_desc', '')
            album.save()
            files = []  #上傳相片串列
            descs = []  #相片說明串列
            picurl = ["ap_picurl1", "ap_picurl2", "ap_picurl3", "ap_picurl4", "ap_picurl5"]
            subject = ["ap_subject1", "ap_subject2", "ap_subject3", "ap_subject4", "ap_subject5"]
            for count in range(0,5):
                files.append(request.FILES.get(picurl[count], ''))
                descs.append(request.POST.get(subject[count], ''))
            i = 0
            for upfile in files:  
                if upfile != '' and descs[i] != '':
                    fs = FileSystemStorage()  #上傳檔案
                    filename = fs.save(upfile.name, upfile)
                    unit = models.PhotoModel.objects.create(palbum=album, psubject=descs[i], purl=upfile)  #寫入資料庫
                    unit.save()
                    i += 1
            return redirect('/adminfix/' + str(album.id) + '/')
        elif deletetype == 'update':  #更新相片說明
            photo = models.PhotoModel.objects.get(id=photoid)
            photo.psubject = request.POST.get('ap_subject', '')  #取得相片說明
            photo.save()  #存寫入資料庫
            return redirect('/adminfix/' + str(album.id) + '/')
        elif deletetype=='delete':  #刪除相片
            photo = models.PhotoModel.objects.get(id=photoid)
            os.remove(os.path.join(settings.MEDIA_ROOT, photo.purl ))  #刪除相片檔
            photo.delete()  #從資料庫移除
            return redirect('/adminfix/' + str(album.id) + '/')
    return render(request, "adminfix.html", locals())
