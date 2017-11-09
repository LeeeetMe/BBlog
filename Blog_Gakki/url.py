"""myBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from Blog_Gakki.views import my_index,login_register,user_home,editor_content

urlpatterns = [

    url(r'^all/(?P<type_id>\d+).html',my_index.Index,name='title_type'),
    url(r'^login.html$', login_register.Login, name='login'),
    url(r'^logout.html$', login_register.Logout),
    url(r'^(?P<site>\w+)-set.html$', login_register.Setting),

    url(r'^auth_code/', login_register.get_auth_code),
    url(r'^register.html$', login_register.Register),
    url(r'^temp_avatar.html$', login_register.load_tempAvatar),
    url(r'^(?P<site>\w+).html$', user_home.home),
    url(r'^(?P<site>\w+)/content.json$', user_home.get_artlist),
    url(r'^(?P<site>\w+)/(?P<condition>((category)|(tags)|(date)))/(?P<value>\w+-*\w*)/', user_home.filter),
    url(r'^mulit_select/(?P<category_id>\d+)-(?P<tags__nid>\d+)$', my_index.multi_select),

    url(r'^(?P<site>\w+)/article/(?P<value>\d+).html$', user_home.articleContent),
    url(r'^article-comment$', user_home.get_comment),
    url(r'^article-updown$', user_home.up_down),
    url(r'^(?P<site>\w+)/(?P<art_id>\d+)/editor-article.html', editor_content.editor),

    url(r'^(?P<site>\w+)/create-article.html', editor_content.create_article),
    url(r'^(?P<site>\w+)/article-img.html$', editor_content.article_img),

]
