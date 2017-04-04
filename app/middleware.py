from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.db import connection


class ShowSqlMiddleware(MiddlewareMixin):
    """打印出每次的数据库操作"""
    def process_response(self, request, response):
        if settings.DEBUG:
            for query in connection.queries:
                print(
                    "\033[1;31m[%s]\033[0m \033[1m%s\033[0m" % (query['time'], " ".join(query['sql'].split())))
        return response
