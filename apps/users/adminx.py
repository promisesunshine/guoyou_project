# _*_ coding:utf-8 _*_
__author__ = 'promise'
__date__ = '2017/5/5 下午2:18'
import xadmin
from xadmin import views

from .models import EmailverifyRecord,Banner

class BaseSettings(object):
    #使用主题
    enable_themes = True
    #启用bootswatch
    use_bootswatch = True

class GlobalSettings(object):
    #xadmin设置标题
    site_title = u"陈力管理系统"
    # xadmin设置底部标题
    site_footer = u"promise公司"
    #显示折叠效果
    menu_style ='accordion'

class EmailverifyRecordAdmin(object):
    list_display = ['code','email','send_type','send_time']
    search_fields = ['code','email','send_type']
    list_filter = ['email','send_type','send_time']


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index','add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index','add_time']

xadmin.site.register(EmailverifyRecord,EmailverifyRecordAdmin)
xadmin.site.register(Banner,BannerAdmin)
xadmin.site.register(views.BaseAdminView,BaseSettings)
xadmin.site.register(views.CommAdminView,GlobalSettings)
