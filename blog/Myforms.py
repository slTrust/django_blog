#!/usr/bin/env python
#-*- encoding:utf-8 -*-
from django import forms
from django.forms import widgets

from blog.models import UserInfo

from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
# 基于forms组件的注册
class UserForm(forms.Form):
    user = forms.CharField(max_length=32,
                           error_messages={'required':'该字段不能为空'},
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
    #局部钩子 处理用户名是否注册
    def clean_user(self):
        user = self.cleaned_data.get('user')

        user = UserInfo.objects.filter(username=user).first()
        if not user:
            return user

        else:
            raise ValidationError('该用户已注册')

    # 全局钩子处理 两次密码
    def clean(self):
        pwd =self.cleaned_data.get('pwd')
        re_pwd = self.cleaned_data.get('re_pwd')

        if pwd==re_pwd:
            return self.cleaned_data
        else:
            raise ValidationError('两次密码不一致')