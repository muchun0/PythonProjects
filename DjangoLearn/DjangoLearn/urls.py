"""DjangoLearn URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from login import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',views.login),
    path('index/',views.index),
    path('add_book',views.add_book),
    path('search',views.search_book),
    path('delete',views.delete_book),
    path('update',views.update_book),
    path('loverelationshipevaluationscale',views.loverelationshipevaluationscale),
    path('depart_list',views.depart_list),
    #q:为什么这里需要后边加一个‘/’
    path('add/depart/',views.add_depart),
    path('delete/depart/',views.delete_depart),
    path('update/depart/',views.update_depart),
]
