from django.conf.urls import url
from django.views.decorators.cache import cache_page
from . import views

app_name = 'app'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    # (?P<article_id>\d+)为一个组, 其中?P<article_di>中的article_id代表了该组的组名
    url(r'^article/(?P<article_id>\d+)$', cache_page(60 * 15)(views.ArticleDetailView.as_view()), name='detail'),
    url(r"^category/(?P<cate_id>\d+)$", views.CategoryView.as_view(), name='category'),
    url(r'^article/(?P<article_id>\d+)/comment/$', views.CommentView, name='comment'),
    url(r'^search/$', views.blog_search, name='search'),
    url(r'^about_me/$', views.suggest_view, name='about_me'),
    url(r'^tags/(?P<tag_id>\d+)$', views.TagView.as_view(), name='tag'),
    url(r'^thanks/$', views.thanks, name='thanks')
]