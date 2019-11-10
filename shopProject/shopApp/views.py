from django.shortcuts import render
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from shopApp.models import *
from django.contrib import messages


def index(request):
    book_list = Book.objects.all()
    content = {'book_list':book_list}
    return render(request,'shopApp/index.html',content)

# 商品详情
def detail(request,id):
    book_detail = Book.objects.get(id=id)
    book_path = book_detail.pic.path.split('\\')[-1]
    content = {'book_detail':book_detail,'book_path':book_path}

    # 记录用户历史,当前有用户登陆则记录，否则不记录
    if 'username' in request.session:
        username = request.session.get('username')

        history = History.objects.all()
        for usr_history in history:
            if usr_history.user == username and book_detail.name == usr_history.book:
                usr_history.delete()
        history_add = History()
        history_add.user = username
        history_add.book = book_detail.name
        history_add.save()

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


# 加入购物车
def add_cart(request):
    request.encoding='utf-8'

    book_name = ''
    book_num = 1
    username = ''

    if request.POST:
        book_name = request.POST.get('book_name')
        book_num = request.POST.get('book_num')
    if 'username' in request.session:
        username = request.session.get('username')
    else:
        return HttpResponse("请登录<br /> <a href = '/login'> 登陆 </a>")

    cart_book = Cart.objects.all()

    already_in = 0
    for item in cart_book:
        if item.user == username and item.book == book_name:
            item.count = item.count + int(book_num)
            item.save()
            already_in = 1
    if not already_in:
        book_add = Cart()
        book_add.user = username
        book_add.book = book_name
        book_add.count = book_num
        book_add.save()

    return HttpResponseRedirect('/cart')
    
# 购物车,列出购物车中的所有商品
def cart(request):
    username = ''
    if 'username' in request.session:
        username = request.session.get('username')
    else:
        return HttpResponse("请登录<br /> <a href = '/login'> 登陆 </a>")

    # content = {'book_name':[],'book_num':[]}
    # 加入购物车中书的名字和数量
    content = {}
    # 每本书的价格
    price = {}
    # 总金额
    price_sum = 0
    cart_book = Cart.objects.all()
    book_all = Book.objects.all()

    for item in cart_book:
        if username == item.user:
            # content['book_name'].append(item.book)
            # content['book_num'].append(item.count)
            content[item.book] = item.count

            for book in book_all:
                if book.name == item.book:
                    price[item.book] = book.price
                    price_sum = price_sum + int(book.price)*int(item.count)
                    break

    return render(request,'shopApp/cart.html',{'content':content,'price':price,'price_sum':price_sum})

# 用户历史
def history(request):
    username = ''
    if 'username' in request.session:
        username = request.session.get('username')
    else:
        return HttpResponse("请登录<br /> <a href = '/login'> 登陆 </a>")

    history = []
    book = []
    history_all = History.objects.all()
    book_all = Book.objects.all()

    for usr_history in history_all:
        if username == usr_history.user:
            history.insert(0,usr_history.book)
            for book_i in book_all:
                if book_i.name == usr_history.book:
                    book.insert(0,book_i)

    return render(request,'shopApp/history.html',{'history':history,'book':book})

def literature_kind(request):
    book = []
    book_all = Book.objects.all()
    for item in book_all:
        if item.category == 'literature':
            book.append(item)
    return render(request,'shopApp/index.html',{'book_list':book,'class':"文学"})

def success_kind(request):
    book = []
    book_all = Book.objects.all()
    for item in book_all:
        if item.category == 'success':
            book.append(item)
    return render(request,'shopApp/index.html',{'book_list':book,'class':"励志"})

def history_kind(request):
    book = []
    book_all = Book.objects.all()
    for item in book_all:
        if item.category == 'history':
            book.append(item)
    return render(request,'shopApp/index.html',{'book_list':book,'class':"历史"})

def child_kind(request):
    book = []
    book_all = Book.objects.all()
    for item in book_all:
        if item.category == 'child':
            book.append(item)
    return render(request,'shopApp/index.html',{'book_list':book,'class':'儿童'})

def search(request):
    book_name = ''
    if request.POST:
        book_name = request.POST.get('book_name')
    
    book = []
    book_all = Book.objects.all()
    for item in book_all:
        if item.name == book_name:
            book.append(item)
        
    return render(request,'shopApp/index.html',{'book_list':book})

# 删除购物车条目
def cart_del(request):
    book_name = request.GET.get('book_name')
    cart_all = Cart.objects.all()
    for book in cart_all:
        if book.book == book_name:
            book.delete()
            break
    return JsonResponse({'state':'ok'})