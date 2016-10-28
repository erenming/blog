from django.conf.urls import url
from . import views

app_name = 'app'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    # (?P<article_id>\d+)为一个组, 其中?P<article_di>中的article_id代表了该组的组名
    url(r'^article/(?P<article_id>\d+)$', views.ArticleDetailView.as_view(), name='detail'),
    url(r"^category/(?P<cate_id>\d+)$", views.CategoryView.as_view(), name='category'),
    url(r'^article/(?P<article_id>\d+)/comment/$', views.CommentView, name='comment'),
    url(r'^search/$', views.blog_search, name='search'),
    url(r'^about_me$', views.about_me, name='about_me')

]