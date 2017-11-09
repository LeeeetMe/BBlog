#!/usr/bin/env python
# -*- coding: utf-8 -*-
import self as self

__author__ = 'Fade Zhao'
from BBlog.settings import BASE_DIR
from Blog_Gakki import models
from django.forms import Form
from django.forms import widgets
from django.forms import fields
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.db import transaction

from django.contrib.auth.forms import UserCreationForm
from Blog_Gakki.models import userInfo
class login_form(Form):
    username = fields.CharField(max_length=32,
                                widget=widgets.TextInput(attrs={'class':"form-control" ,
                                                                'placeholder':"用户名"}),
                                error_messages={'required': '用户名不能为空',
                                                'max_length':'用户名过长'})
    password = fields.CharField(max_length=64,
                                widget=widgets.PasswordInput(attrs={'class': "form-control",
                                                                'placeholder': "密码"}),
                                error_messages={'required': '密码不能为空',
                                                'max_length':'密码过长'})

    auth_code = fields.CharField(max_length=5,
                                widget=widgets.TextInput(attrs={'class': "form-control",
                                                                'placeholder': "验证码"}),
                                 error_messages={'required': '验证码不能为空',
                                                 'max_length': 'to lang'})

    def __init__(self,request,*args,**kwargs):
        self.request = request
        super(login_form,self).__init__(*args,**kwargs)

    def clean_auth_code(self):
        if self.request.session.get('auth_code').upper() == self.cleaned_data.get('auth_code').upper():
            return self.cleaned_data
        else:
            raise ValidationError('验证码错误')

class register_form(Form):
    username = fields.CharField(min_length=2,
                                max_length=32,
                                widget=widgets.TextInput(attrs={'class': "form-control",
                                                                'placeholder': "用户名，不得少于4个字符"}),
                                error_messages={'required':'用户名不能为空',
                                                'max_length':'用户名最多32个字符',
                                                'min_length':'用户名最少4个字符'})
    nickname = fields.CharField(min_length=2,
                                max_length=32,
                                widget=widgets.TextInput(attrs={'class': "form-control",
                                                                'placeholder': "昵称，不得少于2个字符"}),
                                error_messages={'required':'用户名不能为空',
                                                'max_length':'昵称最多32个字符',
                                                'min_length':'昵称最少4个字符'})
    password_1 = fields.CharField(min_length=4,
                                max_length=32,
                                widget=widgets.PasswordInput(attrs={'class': "form-control",
                                                                'placeholder': "密码"}),
                                error_messages={'required':'密码不能为空',
                                                'max_length':'密码最多64个字符',
                                                'min_length':'用户名最少6个字符'})
    password_2 = fields.CharField(min_length=4,
                                  max_length=32,
                                  widget=widgets.PasswordInput(attrs={'class': "form-control",
                                                                      'placeholder': "密码"}),
                                  error_messages={'required': '密码不能为空',
                                                  'max_length': '密码最多64个字符',
                                                  'min_length': '用户名最少6个字符'})

    user_email = fields.CharField(max_length=120,
                                   widget=widgets.EmailInput(attrs={'class': "form-control",
                                                                    'invalid': "邮箱格式错误",
                                                                    'placeholder': "需要通过邮件激活帐户"}),
                                   error_messages={'required': '邮箱不能为空',
                                                   'max_length': '密码最多64个字符',
                                                   'min_length': '用户名最少6个字符'})

    auth_code = fields.CharField(max_length=5,
                                 widget=widgets.TextInput(attrs={'class': "form-control",
                                                                'placeholder': "验证码"}),
                                 error_messages={'required': '验证码不能为空',
                                                 'max_length': '太长'})

    portrait = fields.CharField(required=False,widget=widgets.TextInput(attrs={'id': "form-portrait"}),)

    def __init__(self,request,*args,**kwargs):
        self.request = request
        super(register_form,self).__init__(*args,**kwargs)

    def save(self):
        portrait = self.cleaned_data.get('portrait')
        username = self.cleaned_data.get('username')
        print('name-====',username)
        if portrait:
            import os,shutil
            # 移动文件到文件夹
            new_file = portrait.replace('temp_avatar','imgs/avatar_img')
            old_path = os.path.join(BASE_DIR,portrait)
            new_path = os.path.join(BASE_DIR,new_file)
            shutil.copyfile(old_path,new_path)
            portrait = new_file
        # 创建用户信息
        userInfo_dict ={
            'username':self.cleaned_data.get('username'),
            'password':self.cleaned_data.get('password_1'),
            'nickname': self.cleaned_data.get('nickname'),
            'email': self.cleaned_data.get('user_email'),
            'portrait': portrait,
        }

        new_user = models.userInfo.objects.create(**userInfo_dict)
        # 创建博客信息
        blog_dict = {
            'title': self.cleaned_data.get('nickname'),
            'site': self.cleaned_data.get('username'),
            'theme': 'default',
            'user': new_user,
        }
        models.Blog.objects.create(**blog_dict)


    def clean_username(self):
        '''验证username字段时进行验证'''
        user_dict = {}
        user_dict['username'] = self.cleaned_data.get('username')
        user_obj = models.userInfo.objects.filter(**user_dict)
        if user_obj:
            raise ValidationError('用户名已存在')
        return self.cleaned_data.get('username')

    def clean_password_2(self):
        if self.cleaned_data.get('password_1') == self.cleaned_data.get('password_2'):
            return self.cleaned_data.get('password_2')
        else:
            raise ValidationError('密码不一致')

    def clean_auth_code(self):
        if self.request.session.get('auth_code').upper() == self.cleaned_data.get('auth_code').upper():
            return self.cleaned_data.get('auth_code')
        else:
            raise ValidationError('验证码错误')


class article_form(Form):

    def __init__(self,request,*args,**kwargs):
        self.request = request
        # self.tag_list = self.get_tag()



        super(article_form,self).__init__(*args,**kwargs)
        self.fields['tag_id'].initial ,self.fields['tag_id'].widget.choices = self.get_tag()

    tag_id = fields.CharField(
        # initial=[1, ],
        # choices=(),
        # widget=widgets.CheckboxSelectMultiple)
        # choices = [(7, 'python'), (8, '前端'), (9, 'web-Django'), (10, 'web-Flash'), (11, '携程'), (12, 'Process')],
        # initial= None,
        # choices = tag_choicse,
        widget = widgets.RadioSelect(attrs={'class': 'tag_list'}))

    title = fields.CharField(max_length=64,
                             widget=widgets.TextInput(attrs={'class': "form-control",
                                                             'placeholder': "标题"}),
                             error_messages={'required':'标题不能为空',
                                             'max_length':'用户名最多64个字符',})

    content = fields.CharField(
                               widget=widgets.Textarea(attrs={'class':'form-control',
                                                              'id':'art-content'}),
                               error_messages={'required':'文章不能为空'})
    def clean_tag_id(self):

        return self.cleaned_data.get('tag_id')

    def get_tag(self):
        '''获取Tag标签'''
        user = self.request.session.get('userInfo')
        tag_list = models.Tag.objects.filter(blog=models.Blog.objects.filter(user=user)).values_list('nid','title')
        print(tag_list)
        return tag_list.first()[0],(tag_list)

    def filter_html(content):
        '''
            过滤script标签
        '''
        from bs4 import BeautifulSoup
        Blacklist = ['script']
        soup = BeautifulSoup(content, 'html.parser')
        for item in soup:
            if item.name in Blacklist:
                item.decompose()
        return soup.decode()

    def clean_content(self):
        '''过滤并返回'''
        content = self.cleaned_data.get('content')
        print(content)
        return content

    def save(self):
        '''保存数据'''
        print(self.cleaned_data)
        user = self.request.session.get('userInfo')
        content = self.cleaned_data.get('content')

        article_dic = {
            'title' : self.cleaned_data.get('title'),
            'summary' : content[30] if len(content) > 30 else content,
            'blog' : models.Blog.objects.filter(user=user).first(),
        }
        try:
            with transaction.atomic():
                article = models.Article.objects.create(**article_dic)
                # article.tags.add(models.Tag.objects.filter(nid=)))
                Article2Tag_idc = {
                    'article':article,
                    'tags_id':int(self.cleaned_data.get('tag_id')),
                }
                models.Article2Tag.objects.get_or_create(**Article2Tag_idc)
                detail_dic = {
                    'content': content,
                    'article': article
                }

                models.ArticleDetail.objects.create(**detail_dic)
        except Exception as e:
            print(e)
            return False
        return True



