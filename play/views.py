import itertools
import math

from django.shortcuts import render, redirect
from django.http import StreamingHttpResponse, HttpResponseRedirect
from index.models import *
from user.models import MyUser
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages



# 歌曲播放页面
def playView(request, song_id):
    # 热搜歌曲
    search_song = Dynamic.objects.select_related('song').order_by('-dynamic_search').all()[:6]
    # 歌曲信息
    song_info = Song.objects.get(song_id=int(song_id))
    # 播放列表
    play_list = request.session.get('play_list', [])
    song_exist = False
    if play_list:
        for i in play_list:
            if int(song_id) == i['song_id']:
                song_exist = True
    if song_exist == False:
        play_list.append({'song_id': int(song_id), 'song_singer': song_info.song_singer, 'song_name': song_info.song_name, 'song_time': song_info.song_time})
    request.session['play_list'] = play_list #存入session
    # 歌词
    if song_info.song_lyrics != '暂无歌词':
        f = open('static/songLyric/' + song_info.song_lyrics, 'r', encoding='utf-8')
        song_lyrics = f.read()
        f.close()

    # 添加播放次数
    # 扩展功能：可使用session实现每天只添加一次播放次数
    dynamic_info = Dynamic.objects.filter(song_id=int(song_id)).first()
    # 判断歌曲动态信息是否存在，存在就在原来基础上加1
    if dynamic_info:
        dynamic_info.dynamic_plays += 1
        dynamic_info.save()
    # 动态信息不存在则创建新的动态信息
    else:
        dynamic_info = Dynamic(dynamic_plays=1, dynamic_search=0, dynamic_down=0, dynamic_like=0,  song_id=song_id)
        dynamic_info.save()

    return render(request, 'play.html', locals())



@login_required(login_url='/user/login.html')
def recommendView(request, song_id):
    # 热搜歌曲
    search_song = Dynamic.objects.select_related('song').order_by('-dynamic_search').all()[:6]
    # 歌曲信息
    song_info = Song.objects.get(song_id=int(song_id))
    # 播放列表
    play_list = request.session.get('play_list', [])
    song_exist = False
    if play_list:
        for i in play_list:
            if int(song_id) == i['song_id']:
                song_exist = True
    if song_exist == False:
        play_list.append(
            {'song_id': int(song_id), 'song_singer': song_info.song_singer, 'song_name': song_info.song_name,
             'song_time': song_info.song_time})
    request.session['play_list'] = play_list  # 存入session
    # 歌词
    if song_info.song_lyrics != '暂无歌词':
        f = open('static/songLyric/' + song_info.song_lyrics, 'r', encoding='utf-8')
        song_lyrics = f.read()
        f.close()
    # 基于内容统计的推荐
    # 推荐相关歌曲 推荐同一类型，同一个歌手，同一语种的歌曲，以及混合综合推荐，查询结果合并
    song_type = Song.objects.values('song_type').get(song_id=int(song_id))['song_type']
    song_singer = Song.objects.values('song_singer').get(song_id=int(song_id))['song_singer']
    song_languages = Song.objects.values('song_languages').get(song_id=int(song_id))['song_languages']
    # 结果根据播放量降序排序
    song_relevant1 = Dynamic.objects.select_related('song').filter(song__song_type=song_type).order_by('-dynamic_plays').all()
    song_relevant2 = Dynamic.objects.select_related('song').filter(song__song_singer=song_singer).order_by('-dynamic_plays').all()
    song_relevant3 = Dynamic.objects.select_related('song').filter(song__song_languages=song_languages ).order_by('-dynamic_plays').all()

    # 同曲风推荐的结果存储进song_relevant_type中
    song_relevant_type = []
    # 存入列表 歌曲推荐只需显示名字，歌手名，专辑封面图即可
    for result in song_relevant1:
        if result.song.song_id != int(song_info.song_id):  # 不存入当前正在播放的歌曲信息
            song_relevant_type.append({'song_id': int(result.song.song_id), 'song_singer': result.song.song_singer,
                                       'song_name': result.song.song_name, 'song_img': result.song.song_img})
    request.session['song_relevant_type'] = song_relevant_type  # 存入session

    # 同歌手推荐的结果存储进song_relevant_singer中
    song_relevant_singer = []
    # 存入列表 歌曲推荐只需显示名字，歌手名，专辑封面图即可,不存入当前正在播放的歌曲信息
    for result in song_relevant2:
        if result.song.song_id != int(song_info.song_id):  # 不存入当前正在播放的歌曲信息
            song_relevant_singer.append({'song_id': int(result.song.song_id), 'song_singer': result.song.song_singer,
                                         'song_name': result.song.song_name, 'song_img': result.song.song_img})
    request.session['song_relevant_singer'] = song_relevant_singer  # 存入session

    # 同语种推荐的结果存储进song_relevant_languages中
    song_relevant_languages = []
    # 存入列表 歌曲推荐只需显示名字，歌手名，专辑封面图即可,不存入当前正在播放的歌曲信息
    for result in song_relevant3:
        if result.song.song_id != int(song_info.song_id):  # 不存入当前正在播放的歌曲信息
            song_relevant_languages.append({'song_id': int(result.song.song_id), 'song_singer': result.song.song_singer,
                                            'song_name': result.song.song_name, 'song_img': result.song.song_img})
    request.session['song_relevant_languages'] = song_relevant_languages  # 存入session
    # 根据song_id查找歌曲信息
    song_info = Song.objects.get(song_id=int(song_id))
    # 基于用户的系统过滤推荐cfUser实现
    # train用来存储用户id:对应收藏歌曲id列表，字典存储
    train = {}
    # 获取所有用户的id
    all_user_list = []
    all_user = MyUser.objects.all().values()  # 获取所有用户信息
    for i in all_user:  # 存储所有用户的Id
        all_user_list.append(int(i["id"]))
    # 分别查询出用户喜欢的歌曲
    for uid in all_user_list:
        temp_current_user = MyUser.objects.get(id=int(uid))
        # 查出关联的所有喜欢的歌曲信息
        liked_song_info_result = temp_current_user.liked_song.all()
        liked_song_info = []  # 收藏歌曲列表
        for result in liked_song_info_result:
            liked_song_info.append(int(result.song_id))
        train[uid] = liked_song_info
    # 得到train数据集包含用户和对应喜爱歌曲信息：{1: [2, 3, 4, 5, 6], 2: [4, 5, 6, 7, 8], 7: [1, 2, 3, 4, 5], 8: [5, 6, 7, 8, 9], 9: [6, 7, 8, 9, 10], 10: [7, 8, 9, 10, 11]}

    # 1. 计算相似度
    W = dict()  # 存储相似度
    current_user = MyUser.objects.get(username=request.user.username)
    current_user_id = current_user.id  # 获取当前用户id
    for u in train.keys():
        for v in train.keys():
            if u == current_user_id:
                continue
            W[u] = len(set(train[u]) & set(train[current_user_id]))
            W[u] /= math.sqrt(len(train[u]) * len(train[v]) * 1.0)

    # 2.推荐和用户最相似的3个用户,将推荐用户感兴趣的推荐给目标用户，去除相同项
    rank = dict()  # 存储歌曲相关度的排序列表,如r[2]存储与歌曲id为2的歌曲的兴趣度
    interacted_items = train[current_user_id]  # 当前用户的收藏列表
    top_k_result = sorted(W.items(), key=lambda item: item[1], reverse=True)[0:3]  # 倒序从大到小输出相似度前三的用户及其相似度
    for r in top_k_result:
        # print(r[1])
        for i in train[r[0]]:  # 计算当前用户对歌曲i的可能兴趣度
            if i in interacted_items:  # 排除当前用户已经收藏过的歌曲
                continue
            rank[i] = 0
            rank[i] += r[1] * 1.0
    # 基于用户的协同过滤推荐的结果存储进song_relevant_overall中
    song_cfrelevant_overall = []
    # 将rank中的歌曲信息存入列表 歌曲推荐只需显示名字，歌手名，专辑封面图即可
    for sid in rank.keys():
        cf_song_info = Song.objects.get(song_id=sid)
        song_cfrelevant_overall.append(
            {'song_id': int(cf_song_info.song_id), 'song_singer': cf_song_info.song_singer,
             'song_name': cf_song_info.song_name, 'song_img': cf_song_info.song_img})
    request.session['song_relevant_overall'] = song_cfrelevant_overall  # 存入session
    messages.success(request, "已为您显示个性化推荐！")
    return render(request, 'play.html', locals())





# 歌曲下载
# 设置用户登录限制
@login_required(login_url='/user/login.html')
def downloadView(request, song_id):
    # 根据song_id查找歌曲信息
    song_info = Song.objects.get(song_id=int(song_id))
    # 添加下载次数
    dynamic_info = Dynamic.objects.filter(song_id=int(song_id)).first()
    # 判断歌曲动态信息是否存在，存在就在原来基础上加1
    if dynamic_info:
        dynamic_info.dynamic_down += 1
        dynamic_info.save()
    # 动态信息不存在则创建新的动态信息
    else:
        dynamic_info = Dynamic(dynamic_plays=0, dynamic_search=0, dynamic_like=0, dynamic_down=1, song_id=song_id)
        dynamic_info.save()
    # 读取文件内容
    file = 'static/songFile/' + song_info.song_file
    def file_iterator(file, chunk_size=512):
        with open(file, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    # 将文件内容写入StreamingHttpResponse对象，并以字节流方式返回给用户，实现文件下载
    filename = str(song_id) + '.mp3'
    response = StreamingHttpResponse(file_iterator(file))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment; filename="%s"' % (filename)
    return response



# 歌曲收藏
# 设置用户登录限制
@login_required(login_url='/user/login.html')
def likeView(request, song_id):
    # 根据song_id查找歌曲信息
    song_info = Song.objects.get(song_id=int(song_id))
    # 为当前用户添加收藏曲目信息
    current_user = MyUser.objects.get(username=request.user.username)
    # 在多对多模型表中添加对应的收藏数据
    current_user.liked_song.add(song_info)
    # 弹出消息提示收藏成功
    messages.success(request, "歌曲收藏成功！")
    # 添加收藏次数
    dynamic_info = Dynamic.objects.filter(song_id=int(song_id)).first()
    # 判断歌曲动态信息是否存在，存在就在原来基础上加1
    if dynamic_info:
        dynamic_info.dynamic_like += 1
        dynamic_info.save()
    # 动态信息不存在则创建新的动态信息
    else:
        dynamic_info = Dynamic(dynamic_plays=0, dynamic_search=0, dynamic_like=1, dynamic_down=0, song_id=song_id)
        dynamic_info.save()
    return HttpResponseRedirect("/play/" + str(song_info.song_id) + ".html")
