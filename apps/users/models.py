# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class UserProfile(AbstractUser):
    nick_name=models.CharField(max_length=50,verbose_name=u"昵称",default="")
    birday = models.DateField(verbose_name=u"生日",null=True,blank=True)
    gender = models.CharField(max_length=6,choices=(("male",u"男"),("female",u"女")),default="female")
    address = models.CharField(max_length=100,verbose_name=u"地址",default="")
    mobile = models.CharField(max_length=11,verbose_name=u"手机号",null=True,blank=True)
    image = models.ImageField(max_length=100,upload_to="image/%Y/%m",default="image/default.png")
    class Meta:
        verbose_name=u"用户信息"
        verbose_name_plural=verbose_name
    def __unicode__(self):
        return self.username

class EmailverifyRecord(models.Model):
    code = models.CharField(max_length=20,verbose_name=u"验证码")
    email = models.EmailField(max_length=50,verbose_name=u"邮箱")
    send_type = models.CharField(max_length=10,verbose_name=u"验证码类型",choices=(("register",u"注册"),("forget",u"找回密码")))
    send_time = models.DateTimeField(default=datetime.now,verbose_name=u"实例化时间")
    class Meta:
        verbose_name=u"邮箱验证码"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{0}({1})'.format(self.code,self.email)
class Banner(models.Model):
    title = models.CharField(max_length=100,verbose_name=u"标题")
    image = models.ImageField(max_length=100,upload_to="banner/%Y/%m",verbose_name=u"轮播图")
    url = models.URLField(max_length=200,verbose_name=u"访问地址")
    index = models.IntegerField(default=100,verbose_name=u"顺序")
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u"访问时间")
    class Meta:
        verbose_name = u"轮播图"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{0}({1})'.format(self.title, self.index)