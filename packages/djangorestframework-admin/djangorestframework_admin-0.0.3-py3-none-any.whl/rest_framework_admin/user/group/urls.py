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

from rest_framework_admin.user.group import views

group_router = routers.DefaultRouter()
group_router.register(r'^groups', views.GroupModelViewSet)

group_related_user_router = routers.DefaultRouter()
group_related_user_router.register(
    r'^users',
    views.GroupRelatedUserModelViewSet,
    basename='group_related_user_router')


urlpatterns = [
    path(r'', include(group_router.urls)),
    re_path(
        r'groups/(?P<group_id>[a-z0-9A-Z\-]{32})/',
        include(
            group_related_user_router.urls)),
]
