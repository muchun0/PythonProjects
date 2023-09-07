from django.contrib import admin
from django.urls import path
from gift import views
from django.contrib.auth.views import PasswordResetView

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('login/',views.login),
    # path('index/',views.index),
    # path('add_book',views.add_book),
    # path('search',views.search_book),
    # path('delete',views.delete_book),
    # path('update',views.update_book),
    # path('loverelationshipevaluationscale',views.loverelationshipevaluationscale),
    # path('depart_list',views.depart_list),
    # #q:为什么这里需要后边加一个‘/’
    # path('add/depart/',views.add_depart),
    # path('delete/depart/',views.delete_depart),
    # path('update/depart/',views.update_depart),
    path('password_reset/',PasswordResetView.as_view,name='password_reset'),
    path('login/',views.login),
    path('register',views.register),
    path('get_captcha',views.get_captcha)
]
