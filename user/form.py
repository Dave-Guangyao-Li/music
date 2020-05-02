# from django.contrib.auth.forms import UserCreationForm
# from .models import MyUser
# from django import forms
# from captcha.fields import CaptchaField
#
# # 定义MyUser的数据表单，用于用户注册
# class MyUserCreationForm(UserCreationForm):
#     # 重写初始化函数，设置自定义字段password1和password2的样式和属性
#     def __init__(self, *args, **kwargs):
#         super(MyUserCreationForm, self).__init__(*args, **kwargs)
#         self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'txt tabInput', 'placeholder':'密码,4-16位数字/字母/特殊符号(空格除外)'})
#         self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'txt tabInput', 'placeholder':'重复密码'})
#     captcha = CaptchaField()
#     class Meta(UserCreationForm.Meta):
#         model = MyUser
#         # 在注册界面添加模型字段：手机号码和密码
#         fields = UserCreationForm.Meta.fields + ('mobile',)
#         # 设置模型字段的样式和属性
#         widgets = {
#             'mobile': forms.widgets.TextInput(attrs={'class': 'txt tabInput', 'placeholder':'手机号'}),
#             'username': forms.widgets.TextInput(attrs={'class': 'txt tabInput', 'placeholder':'用户名'}),
#         }


from django import forms
# 引入验证码的CaptchaField
from captcha.fields import CaptchaField

# 表单
class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # widget=forms.PasswordInput用于指定该字段在form表单里表现为<input type='password' />，也就是密码输入框。
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='验证码')
    # # 用户名
    # username = forms.CharField(required=True, min_length=4, error_messages={'invalid': '用户名长度不能少于四个字符'})
    # # 邮箱
    # email = forms.EmailField(required=True, error_messages={'invalid': '请填写正确的邮箱地址'})
    # # 密码
    # password = forms.CharField(required=True, min_length=6, error_messages={'invalid': '密码不能少于6位'})
    # rePassword = forms.CharField(required=True, min_length=6, error_messages={'invalid': '密码不能少于6位'})
    # # 验证码
    # captcha = CaptchaField(required=True, error_messages={'invalid': '验证码错误'})

class RegisterForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    qq = forms.CharField(label="QQ号", max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    weChat = forms.CharField(label="微信号", max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    mobile = forms.CharField(label="电话号", max_length=11, widget=forms.TextInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='验证码')