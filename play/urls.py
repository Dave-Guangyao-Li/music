from django.urls import path
from . import views
urlpatterns = [
    # 歌曲播放页面
    path('<int:song_id>.html', views.playView, name='play'),
    # 歌曲下载
    path('download/<int:song_id>.html', views.downloadView, name='download'),
    # 歌曲收藏
    path('like/<int:song_id>.html', views.likeView, name='like'),
]