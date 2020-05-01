from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from index.models import *
from user.models import *
from .form import MyUserCreationForm
from django.db.models import Q
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from .form import CaptchaTestForm

# 用户注册与登录
def loginView(request):
    # 表单提交
    if request.method == 'POST':
        user = MyUserCreationForm()
        # form = CaptchaTestForm(request.POST)
        # 判断表单提交是用户登录还是用户注册
        # 用户登录
        if request.POST.get('loginUser', ''):
            loginUser = request.POST.get('loginUser', '')
            password = request.POST.get('password', '')
            # captcha = request.POST.get('captcha', '')
            if MyUser.objects.filter(Q(mobile=loginUser) | Q(username=loginUser)):
                user = MyUser.objects.filter(Q(mobile=loginUser) | Q(username=loginUser)).first()
                if check_password(password, user.password):
                    login(request, user)
                    return redirect('/user/home/1.html')
                else:
                    tips = '密码错误'
            else:
                tips = '用户不存在'
        # 用户注册
        else:
            user = MyUserCreationForm(request.POST)
            if user.is_valid():
                user.save()
                tips = '注册成功'
            else:
                if user.errors.get('username', ''):
                    tips = user.errors.get('username', '注册失败')
                else:
                    tips = user.errors.get('mobile', '注册失败')
    else:
        user = MyUserCreationForm()
    return render(request, 'login.html', locals())

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
