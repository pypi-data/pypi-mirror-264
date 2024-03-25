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

from rest_framework_admin.role import views


permission_router = routers.DefaultRouter()
permission_router.register(r'^permissions', views.PermissionViewSet)


role_router = routers.DefaultRouter()
role_router.register(r'^roles', views.RoleModelViewSet)

role_related_permission_router = routers.DefaultRouter()
role_related_permission_router.register(
    r'^permissions',
    views.RoleRelatedPermissionModelViewSet,
    basename='role_related_permission_router')

role_related_subject_router = routers.DefaultRouter()
role_related_subject_router.register(
    r'^subjects',
    views.RoleRelatedSubjectModelViewSet,
    basename='role_related_subject_router')


urlpatterns = [
    path(r'', include(permission_router.urls)),
    path(r'', include(role_router.urls)),
    re_path(
        r'roles/(?P<role_id>[a-z0-9A-Z\-]{32})/',
        include(
            role_related_permission_router.urls)),
    re_path(
        r'roles/(?P<role_id>[a-z0-9A-Z\-]{32})/',
        include(
            role_related_subject_router.urls)),
    re_path(r'^subjects/$', views.SubjectListAPIView.as_view()),
]
