from django.contrib import admin

# Register your models here.

# admin的使用方式：
'''
在这里进行注册  就可以在后台页面进行数据录入
'''

from blog import models
admin.site.register(models.UserInfo)
admin.site.register(models.Blog)
admin.site.register(models.Category)
admin.site.register(models.Tag)
admin.site.register(models.Article)
admin.site.register(models.ArticleUpDown)
admin.site.register(models.Article2Tag)
admin.site.register(models.Comment)