from django.shortcuts import render,HttpResponse,redirect

# Create your views here.
from django.http import JsonResponse
from django.contrib import auth
from blog.models import UserInfo
from blog import models
from django.db.models import Avg,Max,Min,Count

# 事务模块
from django.db import transaction

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
    article_list = models.Article.objects.all()

    return render(request,'index.html',{'article_list':article_list})

from blog.Myforms import UserForm

def register(request):

    if request.is_ajax():
        print(request.POST)
        form=UserForm(request.POST)

        response={'user':None,'msg':None}
        if form.is_valid():
            response['user']=form.cleaned_data.get('user')
            #验证通过生成一条记录
            user =form.cleaned_data.get('user')
            pwd = form.cleaned_data.get('pwd')
            email = form.cleaned_data.get('email')
            # 头像属于文件  在Files里
            avatar_obj = request.FILES.get('avatar')
            print(avatar_obj)
            # 文件字段  他会默认下载到项目的根目录
            # 优化 传参方式
            # if avatar_obj:
            #     user_obj = UserInfo.objects.create_user(username=user,password=pwd,email=email,avatar=avatar_obj)
            # else:
            #     user_obj = UserInfo.objects.create_user(username=user,password=pwd,email=email)

            extra = {}
            if avatar_obj:
                extra['avatar']=avatar_obj

            user_obj = UserInfo.objects.create_user(username=user, password=pwd, email=email,**extra)


        else:
            print(form.cleaned_data)
            print(form.errors)
            response['msg']=form.errors

        return JsonResponse(response)

    form = UserForm()
    return render(request,'register.html',{'form':form})

def logout(request):
    auth.logout(request)
    return redirect('/login/')

def home_site(request,username,**kwargs):
    '''
    个人站点
    :param request:
    :param username:
    :return:
    '''

    print('username',username)
    print('kwargs',kwargs)

    user = UserInfo.objects.filter(username=username).first()
    # 判断用户是否存在
    if not user:
        pass
        return render(request,'not_found.html')
    # 当前站点对象
    blog = user.blog

    # 当前用户的所有文章
    # 基于对象查询
    # article_list = user.article_set.all()
    # 基于双下划线查询
    article_list = models.Article.objects.filter(user=user)

    if kwargs:
        condition = kwargs.get('condition')
        param = kwargs.get('param')
        if condition =='category':
            article_list = article_listfilter(category__title=param)
        elif condition=='tag':
            article_list = article_list.filter(tags__title=param)
        else:
            year,month = param.split('-')
            article_list = article_list.filter(create_time__year=year,create_time__month=month)

    # 查询每一个分类名称及对应的文章数
    # res = models.Category.objects.values('pk').annotate(c=Count('article__title')).values('title','c')
    # 查询当前站点每一个分类名称以及对象的文章数
    # cate_list = models.Category.objects.filter(blog=blog).values('pk').annotate(c=Count('article__title')).values_list('title','c')

    # 查询当前站点每一个标签以及对应的文章数
    # tag_list = models.Tag.objects.filter(blog=blog).values('pk').annotate(c=Count('article')).values_list('title','c')
    # print(tag_list)

    # 查询当前站点每一个年月的名称及对应的文章数
    '''
    extra函数 特殊查询
    
    mysql 查询date类型里的年月  date_format()
    '''
    # res3 = models.Article.objects.extra(select={"is_recent":"create_time>'2017-09-05'"}).values('title','is_recent')
    # print(res3)

    '''
    res4 = models.Article.objects.extra(select={"y_m_d_date":"date_format(create_time,'%%Y-%%m-%%d')"}).values('title','y_m_d_date')
    print(res4)
    
    res5 = models.Article.objects.extra(select={"y_m_date":"date_format(create_time,'%%Y-%%m')"}).values('y_m_date').annotate(c=Count('nid')).values('y_m_date','c')
    print(res5)
    '''
    # 方式一
    # date_list = models.Article.objects.filter(user=user).extra(select={"y_m_date": "date_format(create_time,'%%Y-%%m')"}).values('y_m_date').annotate(c=Count('nid')).values_list('y_m_date', 'c')
    # print(date_list)

    # 日期查询归档函数 TruncMonth('时间字段')
    '''
    from django.db.models.functions import TruncMonth
    
    Sales.objects
        .annotate(month=TruncMonth('时间字段'))\
        .values('month')\
        .annotate(c=Count('id'))\
        .values('month','c')
    '''
    # 方式二
    # from django.db.models.functions import TruncMonth
    # date_list = models.Article.objects.filter(user=user).annotate(xxx=TruncMonth('create_time')).values('xxx').annotate(c=Count('nid')).values_list('xxx','c')
    # print(date_list)

    # return render(request,'home_site.html',{'username':username,'blog':blog,'article_list':article_list,"tag_list":tag_list,'cate_list':cate_list,'date_list':date_list})
    return render(request,'home_site.html',{'username':username,'blog':blog,'article_list':article_list,})


def get_menu_data(username):
    user = UserInfo.objects.filter(username=username).first()
    # 判断用户是否存在
    # if not user:
    #     pass
    #     return render(request, 'not_found.html')
    # 当前站点对象
    blog = user.blog
    # 查询当前站点每一个分类名称以及对象的文章数
    cate_list = models.Category.objects.filter(blog=blog).values('pk').annotate(c=Count('article__title')).values_list(
        'title', 'c')

    # 查询当前站点每一个标签以及对应的文章数
    tag_list = models.Tag.objects.filter(blog=blog).values('pk').annotate(c=Count('article')).values_list('title', 'c')
    # print(tag_list)

    date_list = models.Article.objects.filter(user=user).extra(
        select={"y_m_date": "date_format(create_time,'%%Y-%%m')"}).values('y_m_date').annotate(
        c=Count('nid')).values_list('y_m_date', 'c')
    return {'blog':blog,'cate_list':cate_list,'tag_list':tag_list,'date_list':date_list}

def article_detail(request,username,article_id):

    # context = get_menu_data(username)
    user = UserInfo.objects.filter(username=username).first()
    blog = user.blog

    article_obj = models.Article.objects.filter(pk=article_id).first()

    # 评论列表
    comment_list = models.Comment.objects.filter(article_id=article_id)

    return render(request,'article_detail.html',locals())

# 点赞处理
import json
from django.db.models import F
from django.http import JsonResponse
def digg(requset):
    print(requset.POST)
    article_id = requset.POST.get('article_id')
    # is_up = requset.POST.get('is_up') # 注意这里是 字符串 true
    is_up = json.loads(requset.POST.get('is_up'))
    #点赞人就是当前登陆人
    user_id =requset.user.pk

    # 优化  如果已经 点赞或者踩了  就不能在进行操作了
    obj = models.ArticleUpDown.objects.filter(user_id=user_id,article_id=article_id).first()
    response = {"state":True}
    if not obj:
        # 赞踩关系表一条数据
        ard = models.ArticleUpDown.objects.create(user_id=user_id,article_id=article_id,is_up=is_up)
        # 文章 表  赞  踩个数增加或减少
        queryset = models.Article.objects.filter(pk=article_id)
        if is_up:
            queryset.update(up_count=F('up_count') + 1)
        else:
            queryset.update(down_count=F('down_count') + 1)
    else:
        response['state'] = False
        response['handled'] = obj.is_up

    return JsonResponse(response)

def comment(request):
    print(request.POST)
    article_id = request.POST.get('article_id')
    pid = request.POST.get('pid')
    content = request.POST.get('content')

    user_id = request.user.pk

    # 事务处理 ——同增同减
    '''
    数据同步
    文章评论数加一
    '''
    with transaction.atomic():
        # 评论记录添加
        comment_obj = models.Comment.objects.create(user_id=user_id,article_id=article_id,content=content,parent_comment_id=pid)
        # 文章评论数加一
        models.Article.objects.filter(pk=article_id).update(comment_count=F('comment_count')+1)


    response={}

    # 序列化的时候 要注意时间 需要先变成字符串
    response['create_time'] = comment_obj.create_time.strftime('%Y-%m-%d %X')
    response['username'] = request.user.username
    response['content'] = comment_obj.content


    # 发送邮件的功能
    '''
    python有个模块email 但是这样用起来就很复杂
    
    django内置了一个 邮件模块 
    
    from django.core.mail import send_mail
    
    在settings里设置邮箱地址
    EMAIL_HOST = 'smtp.exmail.qq.com' #如果是163改成 stmp.163.com
    EMAIL_PORT = 456 # 端口号
    EMAIL_HOST_USER = '' # 账号
    EMAIL_HOST_PASSWORD = '' # 授权码  非你的密码
    # EMAIL_FROM_EMAIL = EMAIL_HOST_USER
    EMAIL_USE_SSL = True # 是否使用证书
    
    '''
    from django.core.mail import send_mail
    from cnblog import settings
    # 文章对象
    article_obj = models.Article.objects.filter(pk=article_id).first()
    # send_mail(
    #     '您的文章%s新增了一条评论'%article_obj.title,  # 标题
    #     content ,# 评论内容
    #     settings.EMAIL_HOST_USER, # 账号
    #     # ['598540392@qq.com']
    #     ['1620853536@qq.com']
    # )
    # 发送邮件是同步的代码  影响提交的效率
    import threading
    threading.Thread(target=send_mail,args=(
        '您的文章%s新增了一条评论' % article_obj.title,  # 标题
        content,  # 评论内容
        settings.EMAIL_HOST_USER,  # 账号
        # ['598540392@qq.com']
        ['1620853536@qq.com']
    ))


    return JsonResponse(response)

def get_comment_tree(request):
    article_id = request.GET.get('article_id')

    #res = models.Comment.objects.filter(article_id=article_id).values('pk','comment','parent_comment_id')
    # res是一个queryset 无法序列化
    # 需要list转化
    res = list(models.Comment.objects.filter(article_id=article_id).order_by('pk').values('pk','content','parent_comment_id'))
    '''
    注意select默认查询的顺序是按 id排序的  
    
    所以 不会出现先有子评论  在有父评论的情况
    
    一定是  先有父评论  再有子评论
    # 稳妥处理就是加上order_by
    models.Comment.objects.filter(article_id=article_id).order_by('pk').values('pk','content','parent_comment_id')
    '''
    # 请务必设置 safe=False 序列化必须设置这个参数
    return JsonResponse(res,safe=False)