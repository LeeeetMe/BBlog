from django.contrib import admin

# Register your models here.

from Blog_Gakki import models

admin.site.register(models.Article)
admin.site.register(models.Article2Tag)
admin.site.register(models.Blog)
admin.site.register(models.userInfo)
admin.site.register(models.userFans)
admin.site.register(models.Tag)
admin.site.register(models.Category)
admin.site.register(models.ArticleDetail)
admin.site.register(models.Comment)
