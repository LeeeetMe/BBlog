#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Fade Zhao'
from django.shortcuts import render,HttpResponse,redirect,reverse
from Blog_Gakki import models
from utils import random_check_code,user_form
from io import BytesIO
from django.core.exceptions import ValidationError
import os,time
#
from django.db.models import Count
def auth_session(func):
    '''
        验证用户session
    '''
    def wrap(request,*args,**kwargs):
        if request.session.get('userInfo'):
            ret = func(request,*args,**kwargs)
            return ret
        else:
            return redirect('/Blog/login.html')
    return wrap
def get_category(blog=None):
    '''
        获取文章分类并返回
    '''
    # print(blog.query)
    # 通过博主信息获取category，因为单独获取会造成多次数据库操作而影响效率，所以通过annotate()进行分组一次获取
    category_list = models.Article.objects.values('category_id','category__title').annotate(count=Count('category__title'))
    print('ar-------------------------------')
    print(category_list.query)
    print(category_list)

    for i in category_list:
        print(i['category__title'],i['count'])

    return category_list

def get_tags(blog=None):
    '''
        获取标签分类并返回
    '''
    # values 中的是分组的类目
    tag_list = models.Article2Tag.objects.values('tags_id','tags__title').annotate(count=Count('tags__title'))
    print(tag_list.query)
    print(tag_list)

    for i in tag_list:
        print(i['tags__title'],i['count'])

    return tag_list

def get_timeArticle(blog=None):
    Tarticle_list = models.Article.objects.extra(select={
        'cTime':'date_format(create_time,"%%Y-%%m")'}).values('cTime').annotate(count=Count('nid'))
    # SELECT(date_format(create_time, "%Y-%m"))
    # AS
    # `cTime`, COUNT(`Blog_Gakki_article`.
    # `nid`) AS
    # `count`
    # FROM
    # `Blog_Gakki_article`
    # WHERE
    # `Blog_Gakki_article`.
    # `blog_id` = 1
    # GROUP
    # BY(date_format(create_time, "%Y-%m"))
    # ORDER
    # BY
    # NULL


    print(Tarticle_list.query)
    for i in Tarticle_list:
        # print(i['create_time'],type(i['create_time']))
        print(i)
    return Tarticle_list

def Index(request,*args,**kwargs):
    '''
        主页
    '''
    # if request.method=="GET":
    type_id = int(kwargs.get('type_id')) if kwargs.get('type_id') else None
    # if type_id:
    #     article_list = models.Article.objects.filter(article_type_id=type_id).all()
    # else:
    #     article_list = models.Article.objects.all()
    condition ={}
    if type_id:
        condition['article_type_id'] = type_id
    article_list = models.Article.objects.filter(**condition).order_by("create_time")
    chioces_list = models.Article.type_choices

    category_list = get_category()
    tag_list = get_tags()
    time_list = get_timeArticle()

    userInfo = request.session.get('userInfo')

    blog = None
    is_login = False
    if userInfo:
        blog = models.Blog.objects.filter(user=userInfo).first()
        is_login = True

    condition ={
        'tags__nid':0,
        'category_id':0

    }
    return render(request,'index.html',
                  {
                      'kwargs':condition,
                      'is_login': is_login,
                      'blog': blog,
                      'userInfo':userInfo,
                      'chioces_list':chioces_list,
                      'article_list':article_list,
                      'type_id':type_id,
                      'category_list':category_list,
                      'tag_list':tag_list,
                      'time_list':time_list,
                  })


def multi_select(request, **kwargs):
    '''主页多重筛选'''
    condition ={}

    for key,val in kwargs.items():
        kwargs[key]=int(val)
        if val != '0':
            condition[key]=val
    print(condition)
    if condition:
        article_list = models.Article.objects.filter(**condition).all()
    else:
        article_list = models.Article.objects.all()

    category_list = get_category()
    tag_list = get_tags()
    time_list = get_timeArticle()

    userInfo = request.session.get('userInfo')

    blog = None
    is_login = False
    if userInfo:
        blog = models.Blog.objects.filter(user=userInfo).first()
        is_login = True

    print(kwargs)
    return render(request,'index.html',
                  {
                      'kwargs':kwargs,
                      'is_login': is_login,
                      'blog': blog,
                      'userInfo':userInfo,
                      'article_list':article_list,
                      'category_list':category_list,
                      'tag_list':tag_list,
                      'time_list':time_list,
                  })
