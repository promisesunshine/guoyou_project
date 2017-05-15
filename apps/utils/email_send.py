# _*_ coding:utf-8 _*_

# python自带库
from random import Random

#django库
from django.core.mail import send_mail

#用户自定义库
from users.models import EmailverifyRecord
from guoyou_project.settings import EMAIL_FROM


# 生成随机字符串
def random_str(randomlength=8):
    str = ''
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    length = len(chars)-1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0,length)]
    return str

# 发送注册邮件
def send_register_email(email,send_type = 'register'):
    email_record = EmailverifyRecord()
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()
    if send_type == "register":
        # 邮件标题
        email_title = "promise注册"
        # 邮件内容
        email_body = "请点击下面链接激活账号：http://127.0.0.1:8000/active/{0}".format(code)
        # django自带发送邮件函数
        send_status = send_mail(email_title,email_body,EMAIL_FROM,[email])
        if send_status:
            pass

    elif send_type == "forget":
        # 邮件标题
        email_title = "promise密码重置"
        # 邮件内容
        email_body = "请点击下面链接重置密码：http://127.0.0.1:8000/reset/{0}".format(code)
        # django自带发送邮件函数
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
