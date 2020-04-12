from django.db import models
from django.contrib.auth.models import AbstractUser
from index.models import Song
class MyUser(AbstractUser):
    qq = models.CharField('QQ号码', max_length=20)
    weChat = models.CharField('微信账号', max_length=20)
    mobile = models.CharField('手机号码', max_length=11, unique=True)
    liked_song = models.ManyToManyField(Song, null=True, blank=True, verbose_name='已收藏歌曲')
    # 设置返回值
    def __str__(self):
        return self.username