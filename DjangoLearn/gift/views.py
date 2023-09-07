from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from gift import models
from gift.utils import gen_random_code,Captcha,gen_md5_digest
from django import forms


# 注册
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('login.html')
    else:
        form = UserCreationForm()
        return render(request,'register.html',{'form':form})
# 登录
# def login(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request,data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request,user)
#             return redirect('index.html')
#     else:
#         form = AuthenticationForm()
#         return render(request,'login.html',{'form':form})
# 权限管理
@login_required
def my_account(request):
    # 只允许登录用户访问该视图
    pass

@staff_member_required
def mange_users(request):
    # 只允许管理员访问该视图
    pass

def get_captcha(request) -> HttpResponse:
    """验证码"""
    captcha_text = gen_random_code()
    request.session['captcha'] = captcha_text
    # 验证码60s超时
    request.session.set_expiry(60)
    image_data = Captcha.instance().generate(captcha_text)
    return HttpResponse(image_data, content_type='image/png')



class LoginForm(forms.Form):
    username = forms.CharField(label='用户名',
                                max_length=10,
                                error_messages={'required': '用户名不能为空'},
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入用户名'}))
    password = forms.CharField(label='密码',
                                max_length=10,
                                error_messages={'required': '密码不能为空'},
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码'}))
    code = forms.CharField(
        label='验证码',
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '验证码'})
    )


def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    else:
        form = LoginForm(request.POST)
        # 校验验证码
        captcha_text =request.session.get('captcha')
        code = request.POST.get('code')
        if not captcha_text:
            form.add_error('code','验证码已过期')
            return render(request, 'login.html', {'form': form})
        elif captcha_text.upper() != code.upper():
            form.add_error('code', '验证码错误')
            return render(request, 'login.html', {'form': form})
        elif form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # 对密码进行加密对比
            password_md5 = gen_md5_digest(password)
            user = models.UserInfo.objects.filter(username=username, password=password_md5).first()
            if user:
                # 登录成功，session信息保存7天
                request.session['Info'] = {'name':username}
                request.session.set_expiry(60*60*24*7)
                return redirect('/index/')
            else:
                return render(request, 'login.html', {'error': '用户名或密码错误','form':form})
        else:
            return render(request, 'login.html', {'form': form})