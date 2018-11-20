#!/usr/bin/env python
#-*- encoding:utf-8 -*-

from django import template
from blog import models
from django.db.models import Count
register = template.Library()

@register.simple_tag
def mulit_tag(x,y):
    return x*y


# 返回数据加 dom结合一起的 模版
'''
装饰器的参数是一个模版文件
'''
@register.inclusion_tag('data_dom.html')
def get_menu_data_dom(username):
    user = models.UserInfo.objects.filter(username=username).first()
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
    print('--------')
    print(blog)
    return {'username':username,'blog': blog, 'cate_list': cate_list, 'tag_list': tag_list, 'date_list': date_list}