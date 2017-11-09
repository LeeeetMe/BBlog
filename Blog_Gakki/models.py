from django.db import models

# Create your models here.

class userInfo(models.Model):
    nid = models.BigAutoField(primary_key=True)
    username = models.CharField(verbose_name='用户名',max_length=32,unique=True)
    password = models.CharField(verbose_name='密码',max_length=64)
    nickname = models.CharField(verbose_name='昵称',max_length=32)
    email = models.EmailField(verbose_name='邮箱',unique=True)
    portrait = models.ImageField(verbose_name='头像',upload_to='static/imgs/avatar_img',blank=True)
    create_time = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)

    def __str__(self):
        return '%s %s'%(self.nickname,self.username)

class userFans(models.Model):
    user = models.ForeignKey(to='userInfo',to_field='nid',related_name='users')
    follower = models.ForeignKey(to='userInfo',to_field='nid',related_name='followers')
    class Meta:
        unique_together =[
            ('user','follower')
        ]

    def __str__(self):
        return '用户：%s 粉丝： %s'%(self.user.nickname,self.follower.nickname)
class Blog(models.Model):
    '''
    博客信息
    '''
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='博客标题', max_length=64)
    site = models.CharField(verbose_name='博客后缀', max_length=32, unique=True)
    theme = models.CharField(verbose_name='博客主题', max_length=32)
    user = models.OneToOneField(to='userInfo', to_field='nid')  # ForeignKey + unique

    def __str__(self):
        return '%s %s'%(self.title,self.site)

class Category(models.Model):
    '''
        博主文章分类
    '''
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='分类标题',max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客',to='Blog',to_field='nid')
    def __str__(self):
        return '%s'%(self.title)
class Tag(models.Model):
    '''
        文章标签
    '''
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='标签名称',max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客',to=Blog,to_field='nid')

    def __str__(self):
        return '%s'%(self.title)

class Article(models.Model):
    '''
        用户文章概览
    '''
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='文章标题',max_length=128)
    summary = models.CharField(verbose_name='文章简介',max_length=255)
    read_count = models.IntegerField(verbose_name='阅读量',default=0)
    comment_count = models.IntegerField(verbose_name='评论个数',default=0)
    up_count = models.IntegerField(verbose_name='点赞',default=0)
    down_count = models.IntegerField(verbose_name='踩',default=0)
    create_time = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)

    blog = models.ForeignKey(verbose_name='所属博客',to='Blog',to_field='nid')
    category = models.ForeignKey(verbose_name='文章类型',to='Category',to_field='nid',null=True)

    type_choices = [
        (1,'Python'),
        (2,'数据库'),
        (3,'Cocos2d-x'),
        (4,'unity3d'),
    ]
    article_type_id = models.IntegerField(choices=type_choices,default=1)
    tags = models.ManyToManyField(
        to='Tag',
        through='Article2Tag',
        through_fields=('article','tags'),
    )

    def __str__(self):
        return '%s'%(self.title)

class Article2Tag(models.Model):
    '''
        文章标签和种类
    '''
    nid = models.BigAutoField(primary_key=True)
    article = models.ForeignKey(to='Article',to_field='nid')
    tags = models.ForeignKey(to='Tag',to_field='nid')
    class Meta:
        unique_together=[
            ('article','tags'),
        ]

    def __str__(self):
        return '%s %s-%s' % (self.tags.title, self.article.title,self.article.blog.title)


class ArticleDetail(models.Model):
    '''
        文章详细
    '''
    nid = models.BigAutoField(primary_key=True)
    content = models.TextField(verbose_name='文章内容')
    article = models.OneToOneField(verbose_name='所属文章',to='Article',to_field='nid')
    def __str__(self):
        return '%s %s'%(self.article.title,self.article.blog.title)

class Comment(models.Model):
    '''
        文章评论
    '''
    nid = models.BigAutoField(primary_key=True)
    level = models.IntegerField(verbose_name='评论楼层')
    content = models.TextField(verbose_name='评论内容')
    parent = models.IntegerField(verbose_name='所属楼层',default=0)
    create_time = models.DateTimeField(verbose_name='创建时间')#,auto_now_add=True)

    article = models.ForeignKey(to='Article',to_field='nid')
    user = models.ForeignKey(verbose_name='评论人',to='userInfo',to_field='nid')

    def __str__(self):
        return '%s %s->%s'%(self.article.title,self.level,self.parent)

class updown(models.Model):
    user = models.ForeignKey(verbose_name='用户',to='userInfo',to_field='nid')
    article = models.ForeignKey(verbose_name='文章',to='Article',to_field='nid')
    type_choices = [(-1,'踩'),(0,'无'),(1,'赞')]
    updown = models.IntegerField(verbose_name='赞、踩、none',choices=type_choices, default=0)

    class Meta:
        unique_together=[(
            'user','article'
        )]