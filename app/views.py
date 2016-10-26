from django.shortcuts import render
from .models import Article, Category, BlogComment
from .forms import BlogCommentForm
from django.shortcuts import get_object_or_404, redirect, get_list_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
import markdown2, re

# Create your views here.

class IndexView(ListView):
    template_name = 'blog/index.html'
    # 制定获取的model数据列表的名字
    context_object_name = "article_list"

    def get_queryset(self):
        """
        过滤数据，获取已发布文章列表，并转为html格式
        Returns:

        """
        article_list = Article.objects.filter(status='p')
        for article in article_list:
            article.body = markdown2.markdown(article.body,)
        return article_list

    # 为上下文添加额外的变量，以便在模板中访问
    def get_context_data(self, **kwargs):
        kwargs['category_list'] = Category.objects.all().order_by('name')
        return super(IndexView, self).get_context_data(**kwargs)


class ArticleDetailView(DetailView):
    '''
    显示文章详情
    '''
    model = Article
    template_name = 'blog/detail.html'
    context_object_name = "article"

    # pk_url_kwarg用于接受来自url中的参数作为主键
    pk_url_kwarg = 'article_id'

    # 从数据库中获取id为pk_url_kwargs的对象
    def get_object(self, queryset=None):
        obj = super(ArticleDetailView, self).get_object()
        obj.body = markdown2.markdown(obj.body)
        return obj

    # 新增form到上下文
    def get_context_data(self, **kwargs):
        kwargs['comment_list'] = self.object.blogcomment_set.all()
        kwargs['form'] = BlogCommentForm()
        kwargs['category_list'] = Category.objects.all().order_by('name')
        return super(ArticleDetailView, self).get_context_data(**kwargs)


class CategoryView(ListView):
    template_name = 'blog/index.html'
    context_object_name = "article_list"



    def get_queryset(self):
        article_list = Article.objects.filter(category=self.kwargs['cate_id'], status='p')
        for article in article_list:
            article.body = markdown2.markdown(article.body,)
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['category_list'] = Category.objects.all().order_by('name')
        name = get_object_or_404(Category, pk=self.kwargs['cate_id'])
        kwargs['cate_name'] = name

        return super(CategoryView, self).get_context_data(**kwargs)


def CommentView(request, article_id):
    if request.method == 'POST':
        form = BlogCommentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['user_name']
            email = form.cleaned_data['user_email']
            body = form.cleaned_data['body']

            article = get_object_or_404(Article, pk=article_id)
            new_record = BlogComment(user_name=name,
                                 user_email=email,
                                 body=body,
                                article=article)
            new_record.save()
            return redirect('app:detail', article_id=article_id)


def blog_search(request,):

    search_for = request.GET['search_for']

    if search_for:
        results = []
        article_list = get_list_or_404(Article)
        category_list = get_list_or_404(Category)
        for article in article_list:
            if re.findall(search_for, article.title):
                results.append(article)
        for article in results:
            article.body = markdown2.markdown(article.body, )
        return render(request, 'blog/search.html', {'article_list': results,
                                                    'category_list': category_list})
    else:
        return redirect('app:index')
