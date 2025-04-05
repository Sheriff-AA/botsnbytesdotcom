from django.contrib import admin

from .models import GlobalCounter, ArticlePost, Comment, Contact



admin.site.register(ArticlePost)
admin.site.register(GlobalCounter)
admin.site.register(Comment)
admin.site.register(Contact)