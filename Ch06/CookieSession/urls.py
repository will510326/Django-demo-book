"""CookieSession URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from CookieSessionApp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('set_cookie/<str:key>/<str:value>/', views.set_cookie),
    path('set_cookie2/<str:key>/<str:value>/', views.set_cookie2),
    path('get_cookie/<str:key>/', views.get_cookie),
    path('get_allcookies/', views.get_allcookies),
    path('delete_cookie/<str:key>/', views.delete_cookie),

    path('', views.index),
    path('index/', views.index),

    path('set_session/<str:key>/<str:value>/', views.set_session),
    path('get_session/<str:key>/', views.get_session),
    path('get_allsessions/', views.get_allsessions),

    path('vote/', views.vote),
    path('set_session2/<str:key>/<str:value>/', views.set_session2),
    path('delete_session/<str:key>/', views.delete_session),

    path('login/', views.login),
    path('logout/', views.logout),
]
