# _*_ encoding:utf-8 _*_

#django自带库
from django.shortcuts import render,HttpResponse
from django.contrib.auth import authenticate,login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password

#用户自定义库
from .forms import LoginForm,RegisterForm,ForgetPwdForm,ModifyPwdForm
from .models import UserProfile,EmailverifyRecord
from utils.email_send import send_register_email


# Create your views here.
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


#使用类的登陆
class LoginView(View):
    def get(self,request):
        return render(request, 'login.html', {})
    def post(self,request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, "index.html")
                else:
                    return render(request, "login.html", {"msg": "用户未激活"})
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误"})

        else:
            return render(request, "login.html", {"login_form": login_form})


#注册类
class RegisterView(View):
    def get(self,request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self,request):
       register_form = RegisterForm(request.POST)
       if register_form.is_valid():
           user_name = request.POST.get("email","")
           if UserProfile.objects.filter(email=user_name):
               return render(request,"register.html",{"msg":"此邮箱已经注册过","register_form":register_form})
           else:
               pass_word = request.POST.get("password","")
               user_profile = UserProfile()
               user_profile.username = user_name
               user_profile.email = user_name
               user_profile.is_active = False
               user_profile.password = make_password(pass_word)
               user_profile.save()
               #发送邮件
               send_register_email(user_name,"register")
               return render(request,"login.html")
       else:
           return render(request,"register.html",{"register_form":register_form})


# 激活类
class ActiveUserView(View):
    def get(self,request,active_code):
        all_records = EmailverifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")



# 加载找回密码页面并发送邮件
class ForgetPwdView(View):
    def get(self,request):
        forget_form = ForgetPwdForm()
        return render(request,"forgetpwd.html",{'forget_form':forget_form})

    def post(self,request):
        forget_form = ForgetPwdForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email", "")
            send_register_email(email, "forget")
            return render(request, "send_success.html")
        else:
            return render(request,"forgetpwd.html",{'forget_form':forget_form})



# 找回密码
class ResetPwdView(View):
    def get(self,request,active_code):
        all_records = EmailverifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request,"password_reset.html",{"email":email})
        return render(request, "login.html")



class ModifyPwdView(View):
    def post(self,request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pw1 = request.POST.get("password1","")
            pw2 = request.POST.get("password2","")
            email = request.POST.get("email","")
            if pw1!=pw2:
                return render(request, "password_reset.html", {"email": email,"msg":"密码不一致"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pw2)
            user.save()
            return render(request, "login.html")
        else:
            email = request.POST.get("email", "")
            return render(request, "password_reset.html", {"email": email, "modify_form": modify_form})











