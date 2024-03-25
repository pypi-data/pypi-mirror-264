#!/usr/bin/python
# -*- coding:utf-8 -*-
# Email:iamfengdy@126.com
# DateTime:2023/12/8
# Tool:PyCharm

"""  """
__version__ = '0.0.1'
__history__ = """"""

from rest_framework import permissions


class UserModelPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ('selection', 'update_password'):
            return True
        return request.user.is_admin()

    def has_object_permission(self, request, view, obj):
        return request.user.is_admin()


class UserRelatedGroupModelPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_admin():
            return True
        # 仅允许操作用户自己的
        user = view.get_parent_object()
        return request.user.id == user.id

    def has_object_permission(self, request, view, obj):
        if request.user.is_admin():
            return True
        # 仅允许操作用户自己的
        user = view.get_parent_object()
        return request.user.id == user.id
