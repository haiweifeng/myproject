import os
import random
import string
import re
import uuid

import time
from django.contrib.auth.hashers import make_password, check_password
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from captcha.image import ImageCaptcha
from indexapp.models import MyUser
from tools.tools import GetPostValue, hash_code, send_mail


def login_view(request):
    return render(request,"logapp/login.html")


def log_logic(request):
    fromcart = request.session.get("fromcart")
    l = GetPostValue(request, "username","password", "code", "autologin")
    rulemail = "^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$"
    rulephone = "^[1][3,4,5,7,8][0-9]{9}$"
    res = redirect("index:view")
    reindent = redirect("index:indentview")
    print("在登录逻辑中........")
    if not re.match(rulemail, l[0], re.S) and not re.match(rulephone, l[0], re.S):  # 邮箱/手机号格式检测
        if not MyUser.objects.filter(username=l[0]):
            request.session['login'] = 'n'
            return redirect("log:logview")
        else:
            pwd = MyUser.objects.get(username=l[0]).password
            if check_password(l[1],pwd) and MyUser.objects.get(username=l[0]).active:
                if l[3]:
                    print("jinjinijinininc",l[3])
                    res.set_cookie("username", str(l[0].encode("utf-8"), "latin-1"), max_age=60 * 60 * 24 * 7)
                    reindent.set_cookie("username", str(l[0].encode("utf-8"), "latin-1"), max_age=60 * 60 * 24 * 7)
                request.session['username'] = l[0]
                request.session['login'] = 'y'
                if fromcart:
                    del request.session["fromcart"]
                    return reindent
                return res
            request.session['login'] = 'n'
            return redirect("log:logview")
    else:
       if not MyUser.objects.filter(emal=l[0]):
           request.session['login'] = 'n'
           return redirect("log:logview")
       else:
           pwd = MyUser.objects.get(emal=l[0]).password
           if check_password(l[1], pwd) and MyUser.objects.get(emal=l[0]).active:
               if l[3]:
                   print("hahahhasuudhiduh ")
                   res.set_cookie("username", str(l[0].encode("utf-8"), "latin-1"), max_age=60 * 60 * 24 * 7)
               request.session['username'] = l[0]
               request.session['login'] = 'y'
               if fromcart:
                   del request.session["fromcart"]
                   return redirect("index:indentview")
               return redirect("index:view")
           request.session['login'] = 'n'
           return redirect("log:logview")
def log_exit(request):
    res=redirect("index:view")
    res.delete_cookie("username")
    request.session.clear()
    return res


def regist_view(request):

    return render(request,"logapp/register.html")


def reg_logic(request):
    l = GetPostValue(request, "username", "email", "password", "repassword", "code")
    if MyUser.objects.filter(username=l[0]):    #用户昵称重复检测
        return redirect("log:regview")
    rulemail = "^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$"
    rulephone = "^[1][3,4,5,7,8][0-9]{9}$"
    if not re.match(rulemail,l[1],re.S) and not re.match(rulephone,l[1],re.S):  #邮箱/手机号格式检测
        return redirect("log:regview")
    if not l[2]==l[3]:                                  #两次密码校验
        return redirect("log:regview")
    realcode = request.session.get("code")
    if not realcode.lower() == l[4]:        #验证码校验
        return redirect("log:regview")
    l[2] = make_password(l[2])
    code = str(uuid.uuid4()).replace("-","")
    with transaction.atomic():
        MyUser(username=l[0],emal=l[1],password=l[2],code=code).save()
    request.session["username"]=l[0]
    request.session["email"]=l[1]
    send_mail(l[1],code)
    return redirect("log:registok")



def registok_view(request):
    username = request.session.get("username")
    email = request.session.get("email")
    return render(request,"logapp/register ok.html",{"username":username,"email":email})

def getcaptcha(request):
    path = os.path.abspath("logapp/fonts/1.ttf")
    img = ImageCaptcha(fonts=[path])
    code = random.sample(string.ascii_uppercase , 3)
    code_str = "".join(code)
    print(code_str)
    request.session["code"] = code_str
    data = img.generate(code_str)
    return HttpResponse(data, "image/png")
def ajax_username(request):
    username = request.POST.get("username")
    print("uesrname",username)
    if not username:
        return HttpResponse("null")
    elif " " in username:
        return HttpResponse("space")
    with transaction.atomic():
        if MyUser.objects.filter(username=username):
            return HttpResponse("error")
    return HttpResponse("ok")
def ajax_email(request):
    email = request.POST.get("email")
    rulemail = "^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$"
    rulephone = "^[1][3,4,5,7,8][0-9]{9}$"
    print("email",re.match(rulemail,email,re.S))
    print("phone",re.match(rulephone,email,re.S))
    if re.match(rulemail,email,re.S) or re.match(rulephone,email,re.S):
        with transaction.atomic():
            if MyUser.objects.filter(emal=email):
                print("error")
                return HttpResponse("error")
            print("ok")
            return HttpResponse("ok")
    print("syc")
    return HttpResponse("styerror")

def ajax_captcha(request):
    realcode = request.session.get("code")
    usercode = request.POST.get("code")
    print("real",realcode,"user",usercode)
    if realcode.lower() == usercode.lower():
        return HttpResponse("y")
    return HttpResponse("n")


def email_confirm(request):
    code = request.POST.get('code')
    print(code, '1111111ss')
    try:
        confirm = MyUser.objects.get(code=code)
    except:
        return HttpResponse("no")
    now = time.mktime(time.localtime())
    print("now", now)
    print("regtime", confirm.regtime)
    regtime = time.mktime(time.strptime(str(confirm.regtime),"%Y-%m-%d %H:%M:%S"))
    print("regtime",regtime)
    dectime = (now -regtime) / 1000 / 60
    print(dectime)
    if dectime>10:
        return HttpResponse("no")
    confirm.active = True
    confirm.save()
    return HttpResponse("ok")