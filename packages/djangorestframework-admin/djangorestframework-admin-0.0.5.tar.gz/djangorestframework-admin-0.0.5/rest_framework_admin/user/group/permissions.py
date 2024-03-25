#!/usr/bin/python
# -*- coding:utf-8 -*-
# Email:iamfengdy@126.com
# DateTime:2023/12/8
# Tool:PyCharm

"""  """
__version__ = '0.0.1'
__history__ = """"""

from rest_framework import permissions


class GroupModelPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ('selection', ):
            return True
        return request.user.is_admin()

    def has_object_permission(self, request, view, obj):
        if request.user.is_admin():
            return True
        return obj.create_user_id == request.user.id


class GroupRelatedUserModelPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_admin():
            return True
        # 仅允许操作用户自己创建的
        group = view.get_parent_object()
        return request.user.id == group.create_user_id

    def has_object_permission(self, request, view, obj):
        if request.user.is_admin():
            return True
        # 仅允许操作用户自己创建的
        group = view.get_parent_object()
        return request.user.id == group.create_user_id
