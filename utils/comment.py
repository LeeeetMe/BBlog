#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Fade Zhao'
from Blog_Gakki import models
def get_all_comment(article_id):
    comment_list = get_comment_list(article_id)
    print(comment_list)
    comment_div = create_comment_div(comment_list)
    print(comment_div)
    return comment_div

def get_comment_list(article_id):
    '''
        通过文章id获取数据并制作评论列表
        article_id: 文章id
        return: 返回评论列表
    '''
    comment_list = models.Comment.objects.filter(article=article_id).values('user__nickname',
                                                                            'create_time',
                                                                            'level',
                                                                            'parent',
                                                                            'content',).all()
    comment_dict = {}
    new_list = []
    # 以level为key,创建字典
    for item in comment_list:

        comment_dict[item.get('level')] = item
        # 创建子评论
        comment_dict[item.get('level')]['children']=[]

    # 再次循环列表添加子评论
    for item in comment_list:
        parent = item.get('parent')
        if parent > 0:
            comment_dict[parent]['children'].append(item)

    # 将comment_dict中的value添加到新的列表中,并过滤掉有父级评论的楼层
    for key,value in comment_dict.items():
        if value.get('parent') == 0:
            value['create_time'] = value['create_time'].strftime("%Y-%m-%d %H:%M:%S")
            new_list.append(value)
    print(new_list)
    return new_list

def create_comment_div(comment_list):
    '''
    递归创建评论墙，这步为了减少服务端压力，可以完全移植到前端
    comment_list:评论列表 
    return:评论 div
    '''
    comment_div = '<div class="content-in z-depth-2">'
    for item in comment_list:
        content = item.get('content')
        comment_content = '<div class="posts-content markdown-body">'+str(content)+'</div>'
        comment_div += comment_content
        if item.get('children'):
            comment_div +=create_comment_div(item.get('children'))
    comment_div += '</div>'
    return comment_div

