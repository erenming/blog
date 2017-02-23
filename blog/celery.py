from __future__ import absolute_import, unicode_literals
import os
from celery import Celery


# 为celery程序设置DJANGO_SETTINGS_MODULE环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')

app = Celery('blog')

# 从Django的设置文件中导入CELERY设置
app.config_from_object('django.conf:settings', namespace='CELERY')

# 从所有已注册的app中加载任务模块
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
