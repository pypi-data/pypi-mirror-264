#!/usr/bin/python
# -*- coding:utf-8 -*-
# Email:iamfengdy@126.com
# DateTime:2023/11/21
# Tool:PyCharm

"""  """
__version__ = '0.0.1'
__history__ = """"""
__all__ = []

from django.db import migrations

from rest_framework_admin.role.configs import DefaultRoleSubjectRelEnum, DEFAULT_ROLE_SUBJECT_REL_DATA


def forwards_func(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    RoleSubjectRel = apps.get_model("admin_role", "RoleSubjectRel")
    db_alias = schema_editor.connection.alias
    role_subject_rels = []
    for rel_enum in DefaultRoleSubjectRelEnum:
        data = rel_enum.value._asdict()
        data.update(DEFAULT_ROLE_SUBJECT_REL_DATA)
        role_subject_rels.append(RoleSubjectRel(**data))
    RoleSubjectRel.objects.using(db_alias).bulk_create(role_subject_rels)


class Migration(migrations.Migration):

    dependencies = [
        ('admin_role', '0002_create_role'),
    ]

    operations = [
        migrations.RunPython(forwards_func),
    ]
