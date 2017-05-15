# _*_ encoding:utf-8 _*_
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from .models import CityDict,CourseOrg

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .forms import UserAskForm
from courses.models import Course
from operation.models import UserFavorite

# Create your views here.
class OrgListView(View):
    def get(self,request):
        #城市
        city_alls = CityDict.objects.all()
        #机构
        org_alls = CourseOrg.objects.all()
        hot_orgs = org_alls.order_by("-click_nums")
        #传来city_Id
        city_id = request.GET.get("city","")
        if city_id:
            org_alls = org_alls.filter(city_id=int(city_id))

        #机构类别
        category = request.GET.get("ct", "")
        if category:
            org_alls = org_alls.filter(category=category)

        #学习人数和课程数排名
        sort = request.GET.get("sort", "")
        if sort == "students":
            org_alls = org_alls.order_by("-students")
        elif sort == "courses":
            org_alls = org_alls.order_by("-course_nums")

        org_nums = org_alls.count()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(org_alls,2,request=request)
        org_data = p.page(page)
        return render(request,"org-list.html",locals())


class AddUserAskView(View):
    def post(self,request):
       userask_form = UserAskForm(request.POST)
       if userask_form.is_valid():
           user_ask = userask_form.save(commit=True)
           return HttpResponse('{"status":"success"}',content_type="application/json")
       else:
           return HttpResponse('{"status":"fail","msg":"添加出错"}',content_type="applicaton/json")

class OrgHomeView(View):
    """
        机构首页
    """
    def get(self,request,org_id):
        current_page = 'home'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
              if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id,fav_type=2):
                  has_fav=True
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]
        return render(request,'org-detail-homepage.html',locals())

class OrgCourseView(View):
    """
        机构课程
    """
    def get(self,request,org_id):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_courses = course_org.course_set.all()
        return render(request,'org-detail-course.html',locals())

class OrgDescView(View):
    """
        机构介绍
    """
    def get(self,request,org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request,'org-detail-desc.html',locals())


class OrgTeacherView(View):
    """
        机构讲师
    """
    def get(self,request,org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_teacher = course_org.teacher_set.all()
        return render(request,'org-detail-teachers.html',locals())

class AddFavView(View):
    """
        用户收藏和取消收藏
    """
    def post(self,request):
        fav_id = request.POST.get("fav_id",0)
        fav_type = request.POST.get("fav_type",0)
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type="applicaton/json")
        exists_records= UserFavorite.objects.filter(user=request.user,fav_id=int(fav_id),fav_type=int(fav_type))
        if exists_records:
            exists_records.delete()
            return HttpResponse('{"status":"fail","msg":"收藏"}', content_type="applicaton/json")
        else:
            user_fav = UserFavorite()
            if int(fav_type)>0 and int(fav_id)>0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type=int(fav_type)
                user_fav.save()
                return HttpResponse('{"status":"success","msg":"已收藏"}', content_type="applicaton/json")
            else:
                return HttpResponse('{"status":"fail","msg":"收藏出错"}', content_type="applicaton/json")



