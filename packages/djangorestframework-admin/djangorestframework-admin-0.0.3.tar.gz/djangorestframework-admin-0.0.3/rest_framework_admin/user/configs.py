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


class DefaultUserView(NamedTuple):
    id: str
    nickname: str
    is_staff: bool
    is_superuser: bool


class DefaultUserEnum(Enum):
    root = DefaultUserView(
        id='0' * 32,
        nickname='超级管理员',
        is_staff=True,
        is_superuser=True)
    admin = DefaultUserView(
        id='0' * 31 + '1',
        nickname='管理员',
        is_staff=True,
        is_superuser=False)
    user = DefaultUserView(
        id='0' * 30 + '10',
        nickname='内部用户',
        is_staff=True,
        is_superuser=False)
