import hashlib

from django.contrib.auth.models import User
from django.contrib import messages


from django.shortcuts import render, redirect
from index.models import *
from user.models import *
from django.db.models import Q
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from .form import CaptchaTestForm




from django.shortcuts import render, HttpResponse
from user.form import RegisterForm
from user.form import UserForm
from user.models import MyUser
# make_password引入密码加密的函数
from django.contrib.auth.hashers import make_password
# Create your views here.
from utils.email_util import send_email

# 用户注册与登录
def loginView(request):
    # if request.session.get('is_login', None):
    #     return redirect("/user/home/1.html")
    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            # 校验通过后获取数据
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = MyUser.objects.get(username=username)
                if check_password(password, user.password):  # 利用check_password函数进行密码校验，因为数据库中密码已加密，不能直接相比
                    # 将信息存入session
                    login(request, user) # 登录
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.username
                    return redirect('/user/home/1.html')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'login.html', locals())
    # 非POST请求返回给用户一个空表
    login_form = UserForm()
    return render(request, 'login.html', locals())

    # # 表单提交
    # if request.method == 'POST':
    #     form = RegisterFrom()
    # #     user = MyUserCreationForm()
    # #     # form = CaptchaTestForm(request.POST)
    # #     # 判断表单提交是用户登录还是用户注册
    # # 用户登录
    #     if request.POST.get('loginUser', ''):
    #         loginUser = request.POST.get('loginUser', '')
    #         password = request.POST.get('password', '')
    #         if MyUser.objects.filter(Q(email=loginUser) | Q(username=loginUser)):
    #             user = MyUser.objects.filter(Q(email=loginUser) | Q(username=loginUser)).first()
    #             if check_password(password, user.password):
    #                 login(request, user)
    #                 return redirect('/user/home/1.html')
    #             else:
    #                 tips = '密码错误'
    #         else:
    #             tips = '用户不存在'
    # #     # 用户注册
    # #     else:
    # #         user = MyUserCreationForm(request.POST)
    # #         if user.is_valid():
    # #             user.save()
    # #             tips = '注册成功'
    # #         else:
    # #             if user.errors.get('username', ''):
    # #                 tips = user.errors.get('username', '注册失败')
    # #             else:
    # #                 tips = user.errors.get('mobile', '注册失败')
    # # else:
    # #     user = MyUserCreationForm()
    # return render(request, 'login.html', locals())

def registerView(request):
    # if request.session.get('is_login', None):
    #     # 登录状态不允许注册。你可以修改这条原则！
    #     return redirect("/index/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            qq = register_form.cleaned_data['qq']
            weChat = register_form.cleaned_data['weChat']
            mobile = register_form.cleaned_data['mobile']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'register.html', locals())
            else:
                same_name_user = MyUser.objects.filter(username=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'register.html', locals())
                same_email_user = MyUser.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'register.html', locals())

                # 当一切都OK的情况下，创建新用户
                new_user = MyUser.objects.create()
                new_user.username = username
                new_user.password = make_password(password1)  # 使用加密密码
                new_user.email = email
                new_user.qq = qq
                new_user.weChat = weChat
                new_user.mobile = mobile
                # # 账户状态 未激活
                # new_user.is_active = 0
                new_user.save()
                # 弹出消息提示注册成功
                messages.success(request, "恭喜您注册成功，跳转到登陆页面...")
        #         # 发送注册邮件
        #         if send_email(email, send_type='app'):
        #             # 注册邮件发送成功
        #             return HttpResponse('恭喜您注册成功, 激活邮件已发送至您的邮箱, 请登录后进行激活操作')
        #         else:
        #             return HttpResponse('恭喜您注册成功, 激活邮件发送')
        #     # return redirect('login.html')  # 自动跳转到登录页面
        # else:
        #     # 返回form表单
        #     # 返回注册页面, 信息回填, 显示错误信息
        #     return render(request, 'register.html', locals())
                # 重定向到登陆界面
                return HttpResponseRedirect("login.html")
    register_form = RegisterForm()
    return render(request, 'register.html', locals())
    # if request.method == 'GET':
    #     # 构建form对象, 为了显示验证码
    #     form = RegisterFrom()
    #     return render(request, 'register.html', {'form': form})
    # if request.method == 'POST':
    #     # 验证form提交的数据
    #     form = RegisterFrom(request.POST)
    #     # 判断是否合法
    #     if form.is_valid():
    #         # 判断密码是否一致
    #         username = form.cleaned_data['username']
    #         email = form.cleaned_data['email']
    #         pwd = form.cleaned_data['password']
    #         rePwd = form.cleaned_data['rePassword']
    #         # 两次密码不一致
    #         if pwd != rePwd:
    #             # 返回注册页面和错误信息
    #             # error = '两次密码不一致!'
    #             return render(request, 'register.html', {'form': form, 'error': '两次密码不一致!'})
    #         # 判断用户是否存在
    #         # 根据email查找用户, 如果用户存在, 返回错误信息
    #         if MyUser.objects.filter(email=email):
    #             # 用户已存在
    #             # errMsg = "该用户已存在!"
    #             return render(request, 'register.html', {'form': form, 'errMsg': '该用户已存在!'})
    #         # 创建用户
    #         user = MyUser(username=username, email=email, password=make_password(pwd))
    #         # 对用户传递过来的密码进行加密, 将加密之后的数据进行保存
    #         # 账户状态 未激活
    #         user.is_active = 0
    #         # # 保存为邮箱地址, 可以使用邮箱登录后台
    #         # user.username = email
    #         # 保存用户
    #         user.save()
    #         # 发送注册邮件
    #         if send_email(email, send_type='app'):
    #             # 注册邮件发送成功
    #             return HttpResponse('恭喜您注册成功, 激活邮件已发送至您的邮箱, 请登录后进行激活操作')
    #         else:
    #             return HttpResponse('恭喜您注册成功, 激活邮件发送')
    #     else:
    #         # 返回form表单
    #         # 返回注册页面, 信息回填, 显示错误信息
    #         return render(request, 'register.html', {'form': form})
    # # return render(request, 'register.html', locals())





# 用户中心
# 设置用户登录限制
@login_required(login_url='/user/login.html')
def homeView(request, page):
    # 热搜歌曲
    search_song = Dynamic.objects.select_related('song').order_by('-dynamic_search').all()[:4]
    # 分页功能1
    song_info = request.session.get('play_list', [])
    paginator = Paginator(song_info, 4)
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)

    # 展示用户已收藏歌曲
    # 先查出当前用户所有喜欢的歌曲
    current_user = MyUser.objects.get(username=request.user.username)
    # 查出关联的所有喜欢的歌曲信息
    liked_song_info_result = current_user.liked_song.all()
    liked_song_info = [] # 收藏歌曲列表
    for result in liked_song_info_result:
        liked_song_info.append({'song_id': int(result.song_id), 'song_singer': result.song_singer, 'song_name': result.song_name, 'song_time': result.song_time})
    request.session['liked_song_info'] = liked_song_info  # 存入session
    # 分页功能展示已收藏歌曲
    liked_song_paginator = Paginator(liked_song_info, 4)
    try:
        liked_song_contacts = liked_song_paginator.page(page)
    except PageNotAnInteger:
        liked_song_contacts = liked_song_paginator.page(1)
    except EmptyPage:
        liked_song_contacts = liked_song_paginator.page(liked_song_paginator.num_pages)

    return render(request, 'home.html', locals())

# 取消当前用户的某歌曲收藏
# 设置用户登录限制
@login_required(login_url='/user/login.html')
def unlikeView(request, song_id):
    # 查询当前用户
    current_user = MyUser.objects.get(username=request.user.username)
    current_liked_song_id = current_user.liked_song.get(song_id=int(song_id))
    # 在多对多模型表中删除当前歌曲对应的收藏记录
    current_user.liked_song.remove(current_liked_song_id)
    return HttpResponseRedirect('/user/home/1.html')


# 退出登录
def logoutView(request):
    logout(request)
    return redirect('/')

# ajax接口，实现动态验证验证码
from django.http import JsonResponse, HttpResponseRedirect
from captcha.models import CaptchaStore
def ajax_val(request):
    if request.is_ajax():
        # 用户输入的验证码结果
        response = request.GET['response']
        # 隐藏域的value值
        hashkey = request.GET['hashkey']
        cs = CaptchaStore.objects.filter(response=response, hashkey=hashkey)
        # 若存在cs，则验证成功，否则验证失败
        if cs:
            json_data = {'status':1}
        else:
            json_data = {'status':0}
        return JsonResponse(json_data)
    else:
        json_data = {'status':0}
        return JsonResponse(json_data)

# # 实现密码加密
# def hash_code(s, salt='mysite_login'):
#     h = hashlib.sha256()
#     s += salt
#     h.update(s.encode())  # update方法只接收bytes类型
#     return h.hexdigest()