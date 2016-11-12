## 个人博客


### 基于django1.10以及bootstrap3.0 ###
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
		obj.body = markdown2.markdown(obj.body)
		return obj
	......
```
####记录于2016-10-28

------------

>今天为我的博客添加了标签云的功能，其实现原理与目录实现原理基本一致,不同点在于，与Article数据库的关系变成了ManyToMany类型
#### 记录于2016-11-12

------------


  [2]: http://182.254.129.224/