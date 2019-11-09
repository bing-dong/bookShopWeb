from django.contrib import admin
from shopApp.models import *
# Register your models here.

# 后台中 每个条目显示多个属性
class CartAdmin(admin.ModelAdmin):
    list_display = ['user','book','count']

class HistoryAdmin(admin.ModelAdmin):
    list_display = ['user','book']

# 后台管理条目注册
admin.site.register(User)
admin.site.register(Book)
admin.site.register(Cart,CartAdmin)
admin.site.register(History,HistoryAdmin)