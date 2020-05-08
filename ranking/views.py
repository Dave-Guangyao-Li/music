from django.shortcuts import render
from index.models import *
def rankingView(request):
    # 搜索歌曲
    search_song = Dynamic.objects.select_related('song').order_by('-dynamic_search').all()[:4]
    # 歌曲分类列表
    All_list_type = Song.objects.values('song_type').distinct()
    # 歌曲标签列表
    All_list_label = Song.objects.values('label_id').distinct()
    # 歌曲语种列表
    All_list_language = Song.objects.values('song_languages').distinct()
    # 歌曲列表信息
    song_type = request.GET.get('type', '')
    song_label = request.GET.get('label', '')
    song_language = request.GET.get('language','')
    if song_type:
        song_info = Dynamic.objects.select_related('song').filter(song__song_type=song_type).order_by('-dynamic_plays').all()[:10]
    elif song_label:
        song_info = Song.objects.select_related('label').filter(label__label_id=int(song_label)).order_by('-dynamic__dynamic_plays').all()[:10]
    elif song_language:
        song_info = Dynamic.objects.select_related('song').filter(song__song_languages=song_language).order_by('-dynamic_plays').all()[:10]
    else:
        song_info = Dynamic.objects.select_related('song').order_by('-dynamic_plays').all()[:10]
    return render(request, 'ranking.html', locals())



# 通用视图
from django.views.generic import ListView
class RankingList(ListView):
    # context_object_name设置Html模版的某一个变量名称
    context_object_name = 'song_info'
    # 设定模版文件
    template_name = 'ranking.html'
    # 查询变量song_info的数据
    def get_queryset(self):
        # 获取请求参数
        song_type = self.request.GET.get('type', '')
        song_language = self.request.GET.get('language', '')
        if song_type:
            song_info = Dynamic.objects.select_related('song').filter(song__song_type=song_type).order_by('-dynamic_plays').all()[:10]
        elif song_language:
            song_info = Dynamic.objects.select_related('song').filter(song__song_languages=song_language).order_by('-dynamic_plays').all()[:10]
        else:
            song_info = Dynamic.objects.select_related('song').order_by('-dynamic_plays').all()[:10]
        return song_info

    # 添加其他变量
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 搜索歌曲
        context['search_song'] = Dynamic.objects.select_related('song').order_by('-dynamic_search').all()[:4]
        # 所有歌曲分类
        context['All_list_type'] = Song.objects.values('song_type').distinct()
        # 所有歌曲语种
        context['All_list_language'] = Song.objects.values('song_languages').distinct()
        return context