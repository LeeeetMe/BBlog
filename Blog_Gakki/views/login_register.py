#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Fade Zhao'

from django.shortcuts import render,HttpResponse,redirect,reverse
from Blog_Gakki import models
from Blog_Gakki.views import my_index
from utils import random_check_code,user_form
from io import BytesIO
from django.core.exceptions import ValidationError
import os,time

def Login(request):
    '''
        登陆
    '''
    if request.method=='GET':
        form_obj = user_form.login_form(request)
        return render(request,'login.html',{'form_obj':form_obj})
    else:
        login_obj = user_form.login_form(request,request.POST)
        if login_obj.is_valid():
            # 开启验证
            login_obj.cleaned_data.pop('auth_code')
            login_dict = login_obj.cleaned_data
            user_obj = models.userInfo.objects.filter(**login_dict).first()
            if user_obj:
                print(user_obj)
                request.session['userInfo'] = user_obj
                # 返回带有用户选项的界面
                # 获取用户blog
                # blog = models.Blog.objects.filter(user=user_obj).first()

                return redirect('/')
            else:
                login_obj.add_error('username',ValidationError('用户名或密码错误'))
        else:
            print(login_obj.errors)
        return render(request,'login.html',{'form_obj':login_obj})
def Logout(request):
    '''
        注销
    '''
    user = request.session.get('userInfo')
    if user:
        del request.session['userInfo']
    return redirect('/')


def Register(request):
    '''
        注册
    '''
    if request.method=='GET':
        form_obj = user_form.register_form(request)
        return render(request,'register.html',{'form_obj':form_obj})
    else:
        form_obj = user_form.register_form(request,request.POST)
        if form_obj.is_valid():
            form_obj.cleaned_data.pop('auth_code')
            print(form_obj.cleaned_data.get('username'))
            form_obj.save()
            print(form_obj.cleaned_data)
            return redirect('/')
        else:
            return render(request, 'register.html', {'form_obj': form_obj})

def load_tempAvatar(request):
    '''
        IE10以前版本上传图片预览
    '''
    print(request)
    src = get_Avatar(request,'temp_avatar')
    return HttpResponse(src)

def get_auth_code(request):
    '''
        获取->返回验证码
    '''
    auth_img,auth_code= random_check_code.check_code()
    stream = BytesIO()
    auth_img.save(stream,'png')
    print(auth_code,'验证嘛嘛嘛')
    request.session['auth_code']=auth_code
    return HttpResponse(stream.getvalue())


def get_Avatar(req,_path):
    '''
        保存上传图片并返回路径
    '''
    file_obj = req.FILES.get('Avatar')  # 获取文件
    print('file_obj_name ======',file_obj.name)
    file_name = str(time.time()).replace('.','')+file_obj.name
    file_path = os.path.join('static',_path,file_name)
    with open(file_path, 'wb') as f:  # 写入文件
        for chunk in file_obj.chunks():
            f.write(chunk)
    return file_path  # 返回文件路径，以便HTML端浏览


def Setting(request,*args,**kwargs):
    '''
        设置界面
    '''
    return render(request,'settings.html')