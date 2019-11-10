from django.urls import path
from shopApp.views import *

from django.conf.urls import url
from django.views.static import serve
from shopProject import settings

urlpatterns = [
    path('', index),
    path('<int:id>/', detail),
    path('regist',regist),
    path('login',login),
    path('login_post',login_post),
    path('regist_post',regist_post),
    path('verifyUser',verifyUser),
    path('history',history),
    path('cart',cart),
    path('logout',logout),
    path('verifyLogin',verifyLogin),
    path('literature_kind',literature_kind),
    path('success_kind',success_kind),
    path('history_kind',history_kind),
    path('child_kind',child_kind),
    path('add_cart',add_cart),
    path('search',search),

    # 加载media中的图片
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})
]