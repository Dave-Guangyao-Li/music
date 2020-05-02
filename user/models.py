from django.db import models
from django.contrib.auth.models import AbstractUser
from index.models import Song
class MyUser(AbstractUser):
    qq = models.CharField('QQ号码', max_length=20)
    weChat = models.CharField('微信账号', max_length=20)
    mobile = models.CharField('手机号码', max_length=11, unique=True)
    liked_song = models.ManyToManyField(Song, null=True, blank=True, verbose_name='已收藏歌曲') #多对多模型，存储用户与收藏歌曲
    # 设置返回值
    def __str__(self):
        return self.username


# 定义一个邮件数据模型, 添加需要的字段
from datetime import datetime

# 邮箱验证类
class EmailVeriRecord(models.Model):
    # 验证码
    code = models.CharField(max_length=20, verbose_name='验证码')
    # 用户邮箱
    email = models.EmailField(max_length=50, verbose_name='用户邮箱')
    # datetime.now 在创建对象的时候, 再执行函数获取时间
    # 发送时间
    send_time = models.DateTimeField(default=datetime.now, verbose_name='发送时间', null=True, blank=True)
    # 过期时间
    exprie_time = models.DateTimeField(null=True)
    # 邮件类型
    # choices 枚举选项, 必须从指定的项中选择一个
    email_type = models.CharField(choices=(('register', '注册邮件'), ('forget', '找回密码')), max_length=10)
    class Meta:
        verbose_name = '邮件验证码'
        verbose_name_plural = verbose_name