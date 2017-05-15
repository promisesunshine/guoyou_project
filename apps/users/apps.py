# _*_ coding:utf-8 _*_
from __future__ import unicode_literals

from django.apps import AppConfig

#app在xamin栏显示为用户信息
class UsersConfig(AppConfig):
    name = 'users'
    verbose_name = u"用户信息"
