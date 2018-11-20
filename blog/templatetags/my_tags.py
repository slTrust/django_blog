#!/usr/bin/env python
#-*- encoding:utf-8 -*-

from django import template

register = template.Library()

@register.simple_tag
def mulit_tag(x,y):
    return x*y