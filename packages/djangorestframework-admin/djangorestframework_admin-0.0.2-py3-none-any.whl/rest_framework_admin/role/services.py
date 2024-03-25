#!/usr/bin/python
# -*- coding:utf-8 -*-
# Email:iamfengdy@126.com
# DateTime:2024/3/6
from rest_framework_admin.role.configs import SubjectTypeEnum
from rest_framework_admin.role.models import Role, RoleSubjectRel
from rest_framework_util.services import BaseService


class UserService(BaseService):
    """ 用户角色服务 """

    def filter_roles(self, is_valid=None):
        """ 过滤直接绑定的角色 """
        return Role.filter_by_subject(
            self.id, SubjectTypeEnum.user.name, is_valid=is_valid)

    def save_roles(self, role_ids, **kwargs):
        RoleSubjectRel.save_by_subject(
            self.id, role_ids, SubjectTypeEnum.user.name, **kwargs)

    def delete_roles(self, role_ids):
        RoleSubjectRel.delete_by_subject(
            self.id, role_ids, SubjectTypeEnum.user.name)

    def filter_group_roles(self, is_valid=None):
        """ 过滤通过组绑定的角色 """
        queryset = Role.objects.none()
        for group in self.groups.all():
            queryset = queryset | group.filter_roles(is_valid=is_valid)
        return queryset

    def filter_all_roles(self, is_valid=None, filter_kwargs=None):
        filter_kwargs = filter_kwargs or {}
        user_queryset = self.filter_roles(
            is_valid=is_valid).filter(
            **filter_kwargs)
        group_queryset = self.filter_group_roles(
            is_valid=is_valid).filter(
            **filter_kwargs)
        queryset = user_queryset.union(
            group_queryset, all=True)
        return queryset

    def get_max_role_rel(self):
        """ 获取最大的角色rel """
        role = self.filter_all_roles(is_valid=True).order_by('-weight').first()
        if not role:
            return None
        rel = RoleSubjectRel.objects.get(
            subject_id=role.subject_id,
            subject_type=SubjectTypeEnum.user.name,
            role_id=role.id)
        return rel


class UserGroupService(BaseService):
    def filter_roles(self, is_valid=None):
        """ 过滤直接绑定的角色 """
        return Role.filter_by_subject(
            self.id, SubjectTypeEnum.user_group.name, is_valid=is_valid)

    def save_roles(self, role_ids, **kwargs):
        RoleSubjectRel.save_by_subject(
            self.id, role_ids, SubjectTypeEnum.user_group.name, **kwargs)

    def delete_roles(self, role_ids):
        RoleSubjectRel.delete_by_subject(
            self.id, role_ids, SubjectTypeEnum.user_group.name)
