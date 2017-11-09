#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Fade Zhao'
import json
from django.shortcuts import render,HttpResponse,redirect,reverse
from Blog_Gakki import models
from utils import random_check_code,user_form
from io import BytesIO
from django.core.exceptions import ValidationError
import os,time
from django.db.models import Count,Value
from django.db.models.functions import Concat

from django.db.models import F
from django.db import transaction
from utils.comment import *
def get_category(blog):
    '''
        获取文章分类并返回
    '''
    print(blog)
    # print(blog.query)
    # 通过博主信息获取category，因为单独获取会造成多次数据库操作而影响效率，所以通过annotate()进行分组一次获取
    category_list = models.Article.objects.filter(blog=blog).values('category_id','category__title').annotate(count=Count('category__title'))
    print(category_list.query)
    print(category_list)

    # for i in category_list:
    #     print(i['category__title'],i['count'])

    return category_list

def get_tags(blog):
    '''
        获取标签分类并返回
    '''
    # values 中的是分组的类目
    tag_list = models.Article2Tag.objects.filter(tags__blog=blog).values('tags_id','tags__title').annotate(count=Count('tags__title'))
    print(tag_list.query)
    print(tag_list)

    # for i in tag_list:
        # print(i['tags__title'],i['count'])

    return tag_list

def get_timeArticle(blog):
    Tarticle_list = models.Article.objects.filter(blog=blog).extra(select={
        'cTime':'date_format(create_time,"%%Y-%%m")'}).values('cTime').annotate(count=Count('nid'))
    return Tarticle_list

def home(request,*args,**kwargs):
    use_site = kwargs.get('site')
    blog = models.Blog.objects.filter(site=use_site).first()
    article_list = models.Article.objects.filter(blog=blog).all()
    for item in article_list:
        # print(item.create_time,type(item.create_time))
        item.create_time = item.create_time.strftime("%Y-%m-%d %H:%M:%S")

    category_list = get_category(blog)
    tag_list = get_tags(blog)
    time_list = get_timeArticle(blog)
    # art_new_list =get_content(blog)

    user_blog, is_login = get_userInfo(request)

    return render(request,'user_home.html',
                          {
                              'user': user_blog,
                              'is_login': is_login,
                              'blog':blog,
                              'article_list':article_list,
                              'category_list':category_list,
                              'tag_list':tag_list,
                              'time_list':time_list,
                              # 'art_new_list':art_new_list,
                          })

def get_content(blog):
    '''获取所有文章列表-Tag'''
    article_list = models.Article.objects.filter(blog=blog).values(
        'nid','title','create_time','tags__nid','tags__title').all()

    art_dic = {}
    art_new_list =[]
    for item in article_list:
        print(item['title'])
        if not art_dic.get(item.get('nid')):
            art_dic[item['nid']]= {
                "title":item.get('title'),
                "date":item.get('create_time').strftime("%Y-%m-%d %H:%M:%S"),
                "path":"/Blog/"+blog.site+"/article/"+str(item.get('nid')),
                "tags":[{
                    "name":item.get('tags__title'),
                    "slug":item.get('tags__title'),
                    "permalink":"/Blog/"+blog.site+"/tags/"+str(item.get('tags__nid'))}]
            }
        else:
            tag_item = {
                "name": item.get('tags__title'),
                "slug": item.get('tags__title'),
                "permalink": "/Blog/" + blog.site + "/tags/" + str(item.get('tags__nid'))
            }
            art_dic[item['nid']]["tags"].append(tag_item)

    for k,v in art_dic.items():
        art_new_list.append(v)
    # print('-----------------------')
    # print(art_new_list)
    # print('-----------------------')
    return art_new_list

def get_artlist(request,*args,**kwargs):
    ''' 
    return: 所有文章的列表
    '''
    use_site = kwargs.get('site')
    blog = models.Blog.objects.filter(site=use_site).first()
    ret = get_content(blog)

    return HttpResponse(ret)


def filter(request,site,condition,value):
    ''' 
    site: 博客后缀
    condition: tag、date、category
    value: 分类id
    return: 分类表单
    '''
    blog = models.Blog.objects.filter(site=site).first()
    if not blog:
        return redirect('/')

    article_list = None
    if condition == 'category':
        article_list = models.Article.objects.filter(blog=blog,category=value).all()

    elif condition == 'tags':
        article_list = models.Article.objects.filter(blog=blog,article2tag__tags_id=value).all()
        '''
        ManyToMany：
            字段查询直接通过article表中的tags__id、tag__title跨到tag表中查找
        有第三张关联表：
            通过反向关联
                article2tag__tag: 等同于article2tag__tag_id，并且,可以通过article2tag__tag__nid、article2tag__tag__title获取tag表中的东西
                article2tag__tag_id:获取第三张表的tag__id字段
        '''

    elif condition == 'date':
        article_list = models.Article.objects.filter(blog=blog).extra(where=['date_format(create_time,"%%Y-%%m")=%s'],params=[value,]).all()

    for item in article_list:
        # print(item.create_time,type(item.create_time))
        item.create_time = item.create_time.strftime("%Y-%m-%d %H:%M:%S")

    category_list = get_category(blog)
    tag_list = get_tags(blog)
    time_list = get_timeArticle(blog)
    # art_new_list =get_content(blog)
    user_blog,is_login = get_userInfo(request)

    return render(request,'user_home.html',
                          {
                              'user': user_blog,
                              'is_login':is_login,
                              'blog':blog,
                              'article_list':article_list,
                              'category_list':category_list,
                              'tag_list':tag_list,
                              'time_list':time_list,
                              # 'art_new_list':art_new_list,
                          })


def get_userInfo(request):
    userInfo = request.session.get('userInfo')
    user_blog = None
    is_login = False
    if userInfo:
        print('获取==============userInfo')
        user_blog = models.Blog.objects.filter(user=userInfo).first()
        is_login = True
    else:
        print('没有获取==============userInfo')
    return user_blog,is_login

def articleContent(request,site,value):
    '''
        查看文章,阅读
    '''
    blog = models.Blog.objects.filter(site=site)
    if blog:
        article = models.Article.objects.filter(nid=value).first()
        articleDetail = models.ArticleDetail.objects.filter(article=article).first()

        print(article.title)

    return render(request,'article.html',{
        'article':article,
        'content':articleDetail.content,
    })

def filter_html(content):
    '''
        过滤script标签
    '''
    from bs4 import BeautifulSoup
    Blacklist = ['script']
    soup = BeautifulSoup(content,'html.parser')
    for item in soup:
        if item.name in Blacklist:
            item.decompose()
    return soup.decode()

def get_comment(request):
    '''
        获取评论
    '''
    art_id = request.POST.get('article_id')
    print('文章ID=',art_id,type(art_id))
    comment = get_all_comment(int(art_id))
    print(comment)
    # comment =json.dumps(comment)

    return HttpResponse(comment)

def auth_login(arg):
    '''
        用户操作验证是否登录
    '''
    def outer_warpper(func):
        def warpper(*args, **kwargs):
            print(args,kwargs)
            user = args[0].session.get('userInfo')
            if user:
                res = func(*args, **kwargs)
                return res
            else:
                if arg == 1:
                    response = {'status': -2}
                    return HttpResponse(json.dumps(response))
                elif arg == 2:
                    return redirect(reverse('login'))
        return warpper
    return outer_warpper

@auth_login(1)
def up_down(request):
    '''
        点赞或踩
    '''
    # 是谁点的赞，直接从session中获取user
    # nid为文章id,val->1:赞/0:踩
    # user = request.session.get('userInfo').get('username')
    print('点赞')
    response = {'status': 0, 'msg': '123'}
    art_id = request.POST.get('nid')
    val = int(request.POST.get('val'))
    print('val-type',type(val),val)
    user = request.session.get('userInfo')
    try:
        updown_obj = models.updown.objects.filter(user=user,article__nid=art_id)
        if updown_obj:
            # 已经赞过或者踩过
            print('赞过或者踩过')

        else:
            # 没赞也没踩过
            print('没有赞过或者踩过')
            with transaction.atomic():
                if val:
                    models.Article.objects.filter(nid=art_id).update(up_count=F('up_count')+1)
                    response['status'] = 1
                else:
                    models.Article.objects.filter(nid=art_id).update(down_count=F('down_count')+1)
                    response['status'] = -1
                models.updown.objects.create(user_id=user.nid, article_id=art_id, updown=val)

    except Exception as e:
        response['msg']=e
        response['status'] = 2

    return HttpResponse(json.dumps(response))


