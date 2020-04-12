import itertools

from django.shortcuts import render, redirect
from django.http import StreamingHttpResponse
from index.models import *
from user.models import MyUser
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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

    # 相关歌曲 推荐同一类型，同一个歌手，同一语种的歌曲，查询结果合并
    song_type = Song.objects.values('song_type').get(song_id=int(song_id))['song_type']
    song_singer = Song.objects.values('song_singer').get(song_id=int(song_id))['song_singer']
    song_languages = Song.objects.values('song_languages').get(song_id=int(song_id))['song_languages']
    # 可以自行定义各个字段的权重，并根据播放量排序（同一流派选取3个，同一个歌手选取2个，同一语言选1个）
    song_relevant1 = Dynamic.objects.select_related('song').filter(song__song_type=song_type).order_by('-dynamic_plays').all()[:3]
    song_relevant2 = Dynamic.objects.select_related('song').filter(song__song_singer=song_singer).order_by('-dynamic_plays').all()[:2]
    song_relevant3 = Dynamic.objects.select_related('song').filter(song__song_languages=song_languages).order_by('-dynamic_plays').all()[:1]
    song_relevant_result = set(itertools.chain(song_relevant1, song_relevant2, song_relevant3)) # 合并查询结果并去重
    # 结果存储进song_relevant中
    song_relevant = []
    # 存入列表 歌曲推荐只需显示名字，歌手名，专辑封面图即可
    for result in song_relevant_result:
        song_relevant.append({'song_id': int(result.song.song_id), 'song_singer': result.song.song_singer, 'song_name': result.song.song_name, 'song_img': result.song.song_img})
    request.session['song_relevant'] = song_relevant # 存入session


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
    # 歌词
    if song_info.song_lyrics != '暂无歌词':
        f = open('static/songLyric/' + song_info.song_lyrics, 'r', encoding='utf-8')
        song_lyrics = f.read()
        f.close()
    # 在多对多模型表中添加对应的收藏数据
    current_user.liked_song.add(song_info)
    # 显示推荐歌曲和播放列表
    play_list = request.session.get('play_list')
    song_relevant = request.session.get('song_relevant')
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
    return render(request, 'play.html', locals())
    # return redirect("play/"+ str(song_info.song_id) +".html")