from django.urls import path
from . import views
urlpatterns = [
    # 用户的登录
    path('login.html', views.loginView, name='login'),
    # 用户的注册
    path('register.html', views.registerView, name='register'),
    # 用户中心
    path('home/<int:page>.html', views.homeView, name='home'),
    # 退出用户登录
    path('logout.html', views.logoutView, name='logout'),
    # path('custom.html', views.customView, name='custom'),
    # 验证码验证API接口
    path('ajax_val', views.ajax_val, name='ajax_val'),
    # 取消收藏歌曲
    path('unlike/<int:song_id>.html', views.unlikeView, name='unlike')
]
