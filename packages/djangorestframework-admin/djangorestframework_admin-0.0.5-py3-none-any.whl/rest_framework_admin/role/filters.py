#!/usr/bin/python
# -*- coding:utf-8 -*-
# Email:iamfengdy@126.com
# DateTime:2023/11/16
# Tool:PyCharm

"""  """
__version__ = '0.0.1'
__history__ = """"""

from django_filters import rest_framework as filters

from rest_framework_admin.role.configs import SubjectTypeEnum
from rest_framework_admin.role.models import Role, RolePermissionRel, RoleSubjectRel, Permission


class PermissionFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Permission
        fields = ['name']


class RoleFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    code = filters.CharFilter(lookup_expr='icontains')
    type = filters.CharFilter(method='filter_by_type')
    user_id = filters.CharFilter(method='filter_by_user_id')
    group_id = filters.CharFilter(method='filter_by_group_id')
    # permission_id = filters.CharFilter(method='filter_by_group_id')

    class Meta:
        model = Role
        fields = ['name', 'code', 'type', 'user_id', 'group_id']

    def filter_by_type(self, queryset, name, value):
        return queryset.filter(type__in=value.split(','))

    def filter_by_user_id(self, queryset, name, value):
        queryset = queryset.filter(
            subject_rels__subject_id=value, subject_rels__type=SubjectTypeEnum.user.name)
        return Role.filter_by_valid(queryset, is_valid=True)

    def filter_by_group_id(self, queryset, name, value):
        queryset = queryset.filter(
            subject_rels__subject_id=value, subject_rels__type=SubjectTypeEnum.user_group.name).all()
        return Role.filter_by_valid(queryset, is_valid=True)


class RoleRelatedPermissionFilter(filters.FilterSet):
    id = filters.CharFilter(field_name='permission_id')

    name = filters.CharFilter(
        lookup_expr='icontains',
        field_name='permission__name')

    class Meta:
        model = RolePermissionRel
        fields = ['id', 'name']


class RoleRelatedSubjectFilter(filters.FilterSet):
    id = filters.CharFilter(field_name='subject_id')
    type = filters.CharFilter(field_name='subject_type')

    class Meta:
        model = RoleSubjectRel
        fields = ['id', 'type']
