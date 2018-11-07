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