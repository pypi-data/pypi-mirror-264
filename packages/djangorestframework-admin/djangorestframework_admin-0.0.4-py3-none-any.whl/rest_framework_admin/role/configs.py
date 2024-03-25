#!/usr/bin/python
# -*- coding:utf-8 -*-
# Email:iamfengdy@126.com
# DateTime:2023/11/21
# Tool:PyCharm

"""  """
__version__ = '0.0.1'
__history__ = """"""

from enum import Enum
from typing import NamedTuple

from rest_framework_admin.user.configs import DefaultUserEnum


class SubjectTypeEnum(Enum):
    user = '用户'
    user_group = '用户组'


class RoleTypeEnum(Enum):
    """ 角色类型 """
    builtin = '系统内置'
    custom = '系统自定义'


class DefaultRoleView(NamedTuple):
    id: str
    name: str
    weight: int


class DefaultRoleEnum(Enum):
    owner = DefaultRoleView(id='0' * 31 + '1', name='拥有者', weight=100)
    admin = DefaultRoleView(id='0' * 30 + '10', name='管理员', weight=90)
    user = DefaultRoleView(id='0' * 29 + '100', name='用户', weight=10)


DEFAULT_ROLE_DATA = {
    'create_user_id': DefaultUserEnum.root.value.id,
    'type': RoleTypeEnum.builtin.name
}


class DefaultRoleSubjectRelView(NamedTuple):
    subject_id: str
    role_id: str


class DefaultRoleSubjectRelEnum(Enum):
    owner = DefaultRoleSubjectRelView(
        subject_id=DefaultUserEnum.root.value.id,
        role_id=DefaultRoleEnum.owner.value.id)
    admin = DefaultRoleSubjectRelView(
        subject_id=DefaultUserEnum.admin.value.id,
        role_id=DefaultRoleEnum.admin.value.id)
    user = DefaultRoleSubjectRelView(
        subject_id=DefaultUserEnum.user.value.id,
        role_id=DefaultRoleEnum.user.value.id)


DEFAULT_ROLE_SUBJECT_REL_DATA = {
    'create_user_id': DefaultUserEnum.root.value.id,
    'subject_type': 'user',
}
