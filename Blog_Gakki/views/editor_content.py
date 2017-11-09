#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Fade Zhao'
from django.shortcuts import render,HttpResponse,redirect,reverse
from Blog_Gakki import models
from Blog_Gakki.views import user_home
from utils import user_form
import io,time,os,json
def editor(request,site,art_id):
    '''
        文章编辑
    '''
    return render(request,'createArticle.html')

@user_home.auth_login(2)
def create_article(request,**kwargs):
    '''
        创建文章
    '''
    user = request.session.get('userInfo')
    blog = models.Blog.objects.filter(user=user).first()
    is_login = True

    if request.method == 'GET':
        article_form = user_form.article_form(request)

    else:
        article_form = user_form.article_form(request,request.POST)

        if article_form.is_valid():
            succ = article_form.save()
            if succ:
                new_link ='/Blog/'+ blog.site+'.html'
                return redirect(new_link)
        else:
            print('3',article_form.errors)

    return render(request, 'createArticle.html', {
        'article_obj': article_form,
        'blog': blog,
        'is_login': is_login,
        'userInfo': user
    })

def article_img(request,site):
    '''
        单张图片上传    
    '''
    if request.method == 'POST':
        file_obj = request.FILES.get('imgFile')  # 获取文件
        file_name = site + str(time.time()).replace('.', '') + file_obj.name
        path = 'article_Imgs'
        file_path = os.path.join('static', path, file_name)
        with open(file_path, 'wb') as f:
            for chunk in file_obj.chunks():
                f.write(chunk)

        ret  = {
            'error': 0,
            'url': '/'+file_path,
            'message': '科科',
        }
        return HttpResponse(json.dumps(ret))
