from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.

class Article(models.Model):
    STATUS_CHOICES = (
        ('d', 'part'),
        ('p', 'Published'),
    )   # 文章的状态

    title = models.CharField('标题', max_length=100)
    body = models.TextField('正文')

    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    # auto_now_add : 创建时间戳，不会被覆盖

    last_modified_time = models.DateTimeField('修改时间', auto_now=True)
    # auto_now: 自动将当前时间覆盖之前时间

    status = models.CharField('文章状态', max_length=1, choices=STATUS_CHOICES)
    abstract = models.CharField('摘要', max_length=54, blank=True, null=True,
                                help_text="可选项，若为空格则摘取正文钱54个字符")
    # 阅读量
    views = models.PositiveIntegerField('浏览量', default=0)
    # 点赞数
    likes = models.PositiveIntegerField('点赞数', default=0)
    # 是否置顶
    topped = models.BooleanField('置顶', default=False)
    # 目录分类
    # on_delete 当指向的表被删除时，将该项设为空
    category = models.ForeignKey('Category', verbose_name='分类',
                                 null=True,
                                 on_delete=models.SET_NULL)
    # 标签云
    tags = models.ManyToManyField('Tag', verbose_name='标签集合', blank=True)


    def __str__(self):
        return self.title

    class Meta:
        # Meta 包含一系列选项，这里的ordering表示排序, - 表示逆序
        # 即当从数据库中取出文章时，以文章最后修改时间逆向排序
        ordering = ['-last_modified_time']

    def get_absolute_url(self):
        return reverse('app:detail', kwargs={'article_id': self.pk})

class Category(models.Model):
    """
    另外一个表,储存文章的分类信息
    文章表的外键指向
    """
    name = models.CharField('类名', max_length=20)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间', auto_now=True)

    def __str__(self):
        return self.name

class BlogComment(models.Model):
    user_name = models.CharField('评论者名字', max_length=100)
    body = models.TextField('评论内容')
    created_time = models.DateTimeField('评论发表时间', auto_now_add=True)
    article = models.ForeignKey('Article', verbose_name='评论所属文章', on_delete=models.CASCADE)

    def __str__(self):
        return self.body[:20]

class Tag(models.Model):
    """
    tag(标签云)对应的数据库
    """
    name = models.CharField('标签名', max_length=20)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间', auto_now=True)

    def __str__(self):
        return self.name


class Suggest(models.Model):
    """
    意见存储
    """
    suggest = models.TextField('意见', max_length=200)
    suggest_time = models.DateTimeField('提出时间', auto_now_add=True)

    def __str__(self):
        return self.suggest
