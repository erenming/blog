from django.contrib import admin
from .models import Article, Category, BlogComment

# Register your models here.

admin.site.register([Article, Category, BlogComment, ])
