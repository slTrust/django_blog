from django.shortcuts import render,HttpResponse

# Create your views here.
from django.http import JsonResponse
from django.contrib import auth

def login(request):
    """
        登录视图函数:
           get请求响应页面
           post(Ajax)请求响应字典
        :param request:
        :return:
    """
    if request.method=='POST':
        response = {"user":None,"msg":None}

        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        valid_code = request.POST.get('valid_code')

        # 校验验证码 验证码存在session里  而不是 global里因为 另一个用户访问的时候 就变了
        valid_code_str = request.session.get('valid_code_str')
        if valid_code.upper() == valid_code_str.upper():
            user = auth.authenticate(username=user, password=pwd)
            if user:
                auth.login(request, user)  # request.user== 当前登录对象
                response["user"] = user.username
            else:
                response["msg"] = "用户名或者密码错误!"

        else:
            response["msg"] = "验证码错误!"

        return JsonResponse(response)

    return render(request,'login.html')

# 返回图片验证码
import random
def get_validCode_img(request):

    from blog.utils.validCode import get_valid_code_img
    data = get_valid_code_img(request)
    return HttpResponse(data)

def index(request):
    return render(request,'index.html')


from django import forms
from django.forms import widgets
# 基于forms组件的注册
class UserForm(forms.Form):
    user = forms.CharField(max_length=32,
                           label='用户名',
                           widget=widgets.TextInput(attrs={"class":"form-control"},)
                           )
    pwd = forms.CharField(max_length=32,
                          label='密码',
                           widget=widgets.PasswordInput(attrs={"class":"form-control"},)
                           )
    re_pwd = forms.CharField(max_length=32,
                             label='确认密码',
                           widget=widgets.PasswordInput(attrs={"class":"form-control"},)
                           )
    email = forms.EmailField(max_length=32,
                             label='邮箱',
                           widget=widgets.TextInput(attrs={"class":"form-control"},)
                           )

def register(request):

    if request.is_ajax():
        print(request.POST)
        form=UserForm(request.POST)

        response={'user':None,'msg':None}
        if form.is_valid():
            response['user']=form.cleaned_data.get('user')
        else:
            print(form.cleaned_data)
            print(form.errors)
            response['msg']=form.errors

        return JsonResponse(response)

    form = UserForm()
    return render(request,'register.html',{'form':form})