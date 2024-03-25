#!/usr/bin/python
# -*- coding:utf-8 -*-
# Email:iamfengdy@126.com
# DateTime:2023/11/16
# Tool:PyCharm

"""  """
__version__ = '0.0.1'
__history__ = """"""

from django_filters import rest_framework as filters

from rest_framework_admin.user.models import Group, UserGroupRel


class GroupFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Group
        fields = ['name']


class GroupRelatedUserFilter(filters.FilterSet):
    id = filters.CharFilter(field_name='user_id')

    name = filters.CharFilter(
        lookup_expr='icontains',
        field_name='user__username')

    class Meta:
        model = UserGroupRel
        fields = ['id', 'name']
