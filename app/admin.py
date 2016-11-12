from django.contrib import admin
from .models import Article, Category, BlogComment, Tag

# Register your models here.

admin.site.register([Article, Category, BlogComment, Tag])
