from django.shortcuts import render
from .models import Article, Category, BlogComment, Tag, Suggest
from .forms import BlogCommentForm, SuggestForm
from django.shortcuts import get_object_or_404, redirect, get_list_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
import markdown
import re
import logging
from .tasks import celery_send_email

# Create your views here.

logger = logging.getLogger(__name__)


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
            article.body = markdown.markdown(article.body,)
        return article_list

    # 为上下文添加额外的变量，以便在模板中访问
    def get_context_data(self, **kwargs):
        kwargs['category_list'] = Category.objects.all().order_by('name')
        kwargs['tag_list'] = Tag.objects.all().order_by('name')
        return super(IndexView, self).get_context_data(**kwargs)


class ArticleDetailView(DetailView):
    """
    显示文章详情
    """
    model = Article
    template_name = 'blog/detail.html'
    context_object_name = "article"

    # pk_url_kwarg用于接受来自url中的参数作为主键
    pk_url_kwarg = 'article_id'

    # 从数据库中获取id为pk_url_kwargs的对象
    def get_object(self, queryset=None):
        obj = super(ArticleDetailView, self).get_object()
        # 点击一次阅读量增加一次
        obj.views += 1
        obj.save()
        obj.body = markdown.markdown(obj.body, safe_mode='escape',
        extensions=[
            'markdown.extensions.nl2br',
            'markdown.extensions.fenced_code'
        ])
        return obj

    # 新增form到上下文
    def get_context_data(self, **kwargs):
        kwargs['comment_list'] = self.object.blogcomment_set.all()
        kwargs['form'] = BlogCommentForm()
        kwargs['category_list'] = Category.objects.all().order_by('name')
        kwargs['tag_list'] = Tag.objects.all().order_by('name')
        return super(ArticleDetailView, self).get_context_data(**kwargs)


class CategoryView(ListView):
    template_name = 'blog/index.html'
    context_object_name = "article_list"

    def get_queryset(self):
        article_list = Article.objects.filter(category=self.kwargs['cate_id'], status='p')
        for article in article_list:
            article.body = markdown.markdown(article.body,)
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['category_list'] = Category.objects.all().order_by('name')
        kwargs['tag_list'] = Tag.objects.all().order_by('name')
        name = get_object_or_404(Category, pk=self.kwargs['cate_id'])
        kwargs['cate_name'] = name

        return super(CategoryView, self).get_context_data(**kwargs)


def CommentView(request, article_id):
    if request.method == 'POST':
        form = BlogCommentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['user_name']
            body = form.cleaned_data['body']

            article = get_object_or_404(Article, pk=article_id)
            new_record = BlogComment(user_name=name,
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
            article.body = markdown.markdown(article.body, )
        tag_list = Tag.objects.all().order_by('name')
        return render(request, 'blog/search.html', {'article_list': results,
                                                    'category_list': category_list,
                                                    'tag_list': tag_list})
    else:
        return redirect('app:index')


def thanks(request,):
    return render(request, 'blog/thanks.html')


class TagView(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        """
        根据指定的标签名获得该标签下的全部文章
        """
        article_list = Article.objects.filter(tags=self.kwargs['tag_id'], status='p')
        for article in article_list:
            article.body = markdown.markdown(article.body, extras=['fenced-code-blocks'], )
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['tag_list'] = Tag.objects.all().order_by('name')
        kwargs['category_list'] = Category.objects.all().order_by('name')
        name = get_object_or_404(Tag, pk=self.kwargs['tag_id'])
        kwargs['tag_name'] = name
        return super(TagView, self).get_context_data(**kwargs)


# class SuggestView(FormView):
#     template_name = 'blog/about.html'
#     form_class = SuggestForm
#     success_url = '/thanks/'
#
#     def form_valid(self, form):
#         suggest_data = form.cleaned_data['suggest']
#         obj = Suggest.get_object()
#         obj.suggest = suggest_data
#         obj.save()
#
#         send_mail('访客意见', suggest_data, 'tomming233@sina.com', ['tomming233@163.com'], fail_silently=False)
#         return super(SuggestView, self).form_valid(form)
#
#     def get_context_data(self, **kwargs):
#         kwargs['form'] = SuggestForm()
#         return super(SuggestView, self).get_context_data(**kwargs)


def suggest_view(request):
    form = SuggestForm()
    if request.method == 'POST':
        form = SuggestForm(request.POST)
        if form.is_valid():
            suggest_data = form.cleaned_data['suggest']
            new_record = Suggest(suggest=suggest_data)
            new_record.save()
            try:
                # 使用celery并发处理邮件发送的任务
                celery_send_email.delay('访客意见', suggest_data, 'tomming233@sina.com', ['tomming233@163.com'])
            except Exception as e:
                logger.error("邮件发送失败: {}".format(e))
            return redirect('app:thanks')
    return render(request, 'blog/about.html', {'form': form})

