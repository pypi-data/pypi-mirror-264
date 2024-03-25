#!/usr/bin/python
# -*- coding:utf-8 -*-
# Email:iamfengdy@126.com
# DateTime:2023/11/21
# Tool:PyCharm

""" 创建角色 """
__version__ = '0.0.1'
__history__ = """"""
__all__ = []


from django.db import migrations

from rest_framework_admin.role.configs import DefaultRoleEnum, DEFAULT_ROLE_DATA


def forwards_func(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    Role = apps.get_model("admin_role", "Role")
    db_alias = schema_editor.connection.alias
    roles = []
    for role_enum in DefaultRoleEnum:
        data = role_enum.value._asdict()
        data.update(DEFAULT_ROLE_DATA)
        roles.append(Role(**data))
    Role.objects.using(db_alias).bulk_create(roles)


def reverse_func(apps, schema_editor):
    Role = apps.get_model("admin_role", "Role")
    db_alias = schema_editor.connection.alias
    role_ids = [_.value.id for _ in DefaultRoleEnum]
    Role.objects.using(db_alias).filter(id__in=role_ids).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('admin_role', '0001_initial'),
        ('admin_user', '0002_create_user')
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
