#!/usr/bin/python
# -*- coding:utf-8 -*-
# Email:iamfengdy@126.com
# DateTime:2023/11/17
# Tool:PyCharm

"""  """
__version__ = '0.0.1'
__history__ = """"""
__all__ = ['urlpatterns']

from django.urls import path, include, re_path
from rest_framework import routers

from rest_framework_admin.user import views
from rest_framework_admin.user.group.urls import urlpatterns as group_urlpatterns

user_router = routers.DefaultRouter()
user_router.register(r'^users', views.UserModelViewSet)

user_related_group_router = routers.DefaultRouter()
user_related_group_router.register(
    r'^groups',
    views.UserRelatedGroupModelViewSet,
    basename='user_related_group_router')

urlpatterns = [
    path(r'', include(user_router.urls)),
    re_path(
        r'users/(?P<user_id>[a-z0-9A-Z\-]{32})/',
        include(
            user_related_group_router.urls)),
] + group_urlpatterns
