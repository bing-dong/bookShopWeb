from django.shortcuts import render
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from shopApp.models import *
from django.contrib import messages


def index(request):
    book_list = Book.objects.all()
    content = {'book_list':book_list}
    return render(request,'shopApp/index.html',content)

def detail(request,id):
    book_detail = Book.objects.get(id=id)
    book_path = book_detail.pic.path.split('\\')[-1]
    content = {'book_detail':book_detail,'book_path':book_path}
    return render(request,'shopApp/detail.html',content)

def regist(request):
    user = User.objects.all()
    content = {'user':user}
    return render(request,'shopApp/regist.html',content)

def regist_post(request):
    request.encoding='utf-8'
    user = ''
    password = ''
    if request.POST:
        user = request.POST['user']
        password = request.POST['password']
    
    # # 用户名和密码是否为空
    # if user == '':
    #     # messages.success(request,'请填写用户名')
    #     return HttpResponse("请填写用户名<br /> <a href = '/regist'> 返回 </a>")
    # if password == '':
    #     return HttpResponse("请填写密码<br /> <a href = '/regist'> 返回 </a>")

    #判断用户是否已存在
    user_db = User.objects.all()
    for u in user_db:
        if user == u.name:
            return HttpResponse("用户已存在，请重新填写<br /> <a href = '/regist'> 返回 </a>")
    
    # 存入数据库
    user_add = User()
    user_add.name = user
    user_add.password = password
    user_add.save()

    return HttpResponse("注册成功<br /> <a href = '../'> 返回首页 </a>")

def login(request):
    return render(request,'shopApp/login.html')

def login_post(request):
    request.encoding='utf-8'

    user = ''
    password = ''
    if request.POST:
        user = request.POST['user']
        password = request.POST['password']
    
    # 用户名和密码是否为空
    if user == '':
        # messages.success(request,'请填写用户名')
        return HttpResponse("请填写用户名<br /> <a href = '/login'> 返回 </a>")
    if password == '':
        return HttpResponse("请填写密码<br /> <a href = '/login'> 返回 </a>")

    last_session_usr = request.session.get('username')
    last_session_pw = request.session.get('userpw')

    if user == last_session_usr and password == last_session_pw:
        return HttpResponseRedirect('/')

    # 比对用户名和密码
    user_db = User.objects.all()
    for u in user_db:
        if user == u.name and password == u.password:
            # 登陆成功 保存session
            request.session['username'] = user
            request.session['userpw'] = password
            return HttpResponseRedirect('/')

    return HttpResponse("用户名或密码错误<br /> <a href = '/login'> 返回 </a>")

# ajax判断注册时用户是否存在
def verifyUser(request):
    request.encoding='utf-8'

    # user = ''
    # if request.GET:
    user = request.GET.get('user')

    ret = {'state':'ok'}
    user_db = User.objects.all()
    for u in user_db:
        if user == u.name:
            ret['state'] = 'false'

    return JsonResponse(ret)

# 判断用户是否在ssession中，若在则自动登陆
def verifyLogin(request):
    request.encoding='utf-8'

    ret = {'state':'ok'}
    if 'username' in request.session:
        ret['name'] = request.session['username']
    else:
        ret['state'] = 'false'
    return JsonResponse(ret)

# 登出 删除session
def logout(request):
    if 'username' in request.session:
        del request.session['username']
    if 'userpw' in request.session:
        del request.session['userpw']
    return HttpResponseRedirect('/')

# 用户历史
def history(request):
    pass

# 购物车
def cart(request):
    pass

def literature_kind(request):
    content = {}
    return render(request,'shopApp/index.html',content)

def success_kind(request):
    content = {}
    return render(request,'shopApp/index.html',content)

def history_kind(request):
    content = {}
    return render(request,'shopApp/index.html',content)

def child_kind(request):
    content = {}
    return render(request,'shopApp/index.html',content)