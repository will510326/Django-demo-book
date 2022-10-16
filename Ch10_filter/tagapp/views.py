from django.shortcuts import render

def index(request):  #首頁
	scores = [78, 83, 90, 62, 87, 71]
	return render(request, "index.html", locals())

def tag(request):  #首頁
	subjects = ["國文", "英文", "數學", "自然", "社會"]
	scores = [78, 83, 90, 62, 87]
	return render(request, "tag.html", locals())
