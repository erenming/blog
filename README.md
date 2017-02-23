## 个人博客
 
—— 基于django1.10以及bootstrap3.0
 
----------
### 简介
> 目前博客功能拥有基本的分页、评论、详细阅读的功能
####纪录于2016.10.2

----------

>今天为博客增添了按标题搜索的功能
####纪录于2016-10-7

----------
>历经千辛万苦，终于将博客部署到好了，点击进入[我的博客][2]
####记录于2016-10-26

------------

>今天对博客的页面以及代码进行了优化，同时，添加了阅读量随点击增加的功能
```python
class ArticleDetailView(DetailView):
	......
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
	......
```
####记录于2016-10-28

------------

>今天为我的博客添加了标签云的功能，其实现原理与目录实现原理基本一致,不同点在于，与Article数据库的关系变成了ManyToMany类型
#### 记录于2016-11-12

------------

>今天为我的博客添加了网页意见提出功能, 用户通过在'''关于'''界面的意见栏写下意见, 将意见信息保存到数据库并发送意见给我自己并返回感谢界面
#### 记录于2016-12-8

------------

>由于markdown2不能解析篱笆型代码块，故将其替换为了markdown
#### 记录于2017-02-7

--------

>添加日志配置
#### 记录于2017-02-8

--------

>添加Redis用以缓存文章界面
#### 记录于2017-02-21

--------

>添加[Celery][3]异步处理请求(我用来处理发送邮件时, 可能造成的阻塞(ps.没什么访问量，其实并不会发生- -))
#### 记录于2017-02-21

--------

  [2]: http://182.254.129.224/
  [3]: http://docs.celeryproject.org/en/latest/index.html
