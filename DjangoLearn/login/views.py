from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse


# Create your views here.
def login(request):
    # return HttpResponse('登录页面')
    # 获取请求方法，如果是get,返回login.html,post，则作为表单来处理，判断登录结果
    if request.method == 'GET':
        # return render(request, 'extendslogin.html') ,继承模板
        return render(request, 'login.html')
    else:
        # 判断用户名与密码是否正确
        username = request.POST.get('fm-login-id')
        password = request.POST.get('fm-login-password')
        # 预期通过数据库去查
        if username == 'admin' and password == '123':
            # 默认跳转http://127.0.0.1:8000/index/ 注意index前的‘/’不可省略，否则将跳转http://127.0.0.1:8000/login/index/
            return redirect('/index/')
        else:
            return render(request, 'login.html', {'error': '用户名或密码错误'})


def index(request):
    return render(request, 'index.html')


# 数据库操作
from login import models


# 增加
def add_book(request):
    # 方法1：通过模型实例化增加,参数预期是外部传入
    # book = models.Book(title="菜鸟教程",price=300,publish="菜鸟出版社",pub_date="2008-8-8")
    # book.save()
    # 方法2：通过ORM提供的objects提供的方法create来实现（推荐）
    models.Book.objects.create(title="如来神掌", price=200, publish="功夫出版社", pub_date="2010-10-10")
    return HttpResponse("<p>数据添加成功！</p>")


# 查询
def search_book(request):
    # 查询全表
    # result = models.Book.objects.all()
    # 条件查询
    # 返回的是 QuerySet 类型数据，类似于 list，里面放的是一个个模型类的对象，可用索引下标取出模型类的对象。
    # result = models.Book.objects.filter(title='菜鸟教程')
    # pk=3 的意思是主键 primary key=3，相当于 id=3,因为 id 在 pycharm 里有特殊含义，是看内存地址的内置函数 id()，因此用 pk。
    result = models.Book.objects.filter(pk=3)
    return render(request, 'search.html', {'result': result[0]})


# 修改
def update_book(request):
    # QuerySet 类型数据.update(字段名=更改的数据)（推荐）,返回值：整数，受影响的行数
    # 主键7和8的数据，price修改魏888
    books = models.Book.objects.filter(pk__in=[7, 8]).update(price=888)
    return HttpResponse(books)


# 删除
def delete_book(request):
    # 删除主键1或2的数据，返回值：元组，第一个元素为受影响的行数。
    books = models.Book.objects.filter(pk__in=[1, 2]).delete()
    return HttpResponse("<p>数据删除成功！</p>")

#返回loverelationshipevaluationscale.html
def loverelationshipevaluationscale(request):
    return render(request, 'loverelationshipevaluationscale.html')