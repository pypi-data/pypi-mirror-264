#!/usr/bin/python
# -*- coding:utf-8 -*-
# Email:iamfengdy@126.com
# DateTime:2023/11/16
# Tool:PyCharm
from django.contrib.auth import get_user_model
from django.db import models


from rest_framework_util.db.models.base import BaseModel, BaseRelModel


class Group(BaseModel):
    user_rels = models.ManyToManyField(
        get_user_model(), through='UserGroupRel', through_fields=(
            'group', 'user'), related_name='group_rels')
    expire_datetime = models.DateTimeField('过期时间', blank=True, null=True)

    class Meta:
        db_table = 'admin_user_group'
        verbose_name = '用户组表'

    @property
    def user_count(self):
        return self.user_rels.count()


class UserGroupRel(BaseRelModel):
    user = models.ForeignKey(get_user_model(), models.RESTRICT)
    group = models.ForeignKey(Group, models.RESTRICT)

    class Meta:
        db_table = 'admin_user_group_rel'
        verbose_name = '用户组关联表'
        unique_together = ('user', 'group', 'delete_datetime')

    def extended_strs(self):
        return [f'user_id={self.user.id}', f'group_id={self.group.id})']
