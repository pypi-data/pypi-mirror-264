#!/usr/bin/python
# -*- coding:utf-8 -*-
# Email:iamfengdy@126.com
# DateTime:2023/11/17
# Tool:PyCharm

"""  """
__version__ = '0.0.1'
__history__ = """"""

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from rest_framework_admin.user.models import User, Group, UserGroupRel
from rest_framework_util.serializers import (
    BaseSwitchModelSerializer,
    BaseModelSerializer,
    BaseRelatedModelSerializer,
    BaseSelectionModelSerializer,
    BaseRelModelSerializer)


class GroupModelSerializer(BaseModelSerializer, serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=64, validators=[
            UniqueValidator(
                queryset=Group.objects.filter())])
    user_count = serializers.IntegerField(
        help_text='用户个数', read_only=True)
    expire_ts = serializers.SerializerMethodField()
    expire_datetime = serializers.DateTimeField(
        input_formats='%Y%m%d%H%M', required=False)

    class Meta(BaseModelSerializer.Meta):
        model = Group
        fields = BaseModelSerializer.Meta.fields + \
            ('user_count', 'expire_datetime', 'expire_ts')

    @extend_schema_field(OpenApiTypes.INT)
    def get_expire_ts(self, obj):
        return self.get_ts_by_field(obj, 'expire_datetime')


class RelatedGroupModelSerializer(BaseRelatedModelSerializer):
    class Meta(BaseRelatedModelSerializer.Meta):
        model = Group


class SwitchGroupModelSerializer(BaseSwitchModelSerializer):

    class Meta(BaseSwitchModelSerializer.Meta):
        model = Group


class SelectionGroupModelSerializer(BaseSelectionModelSerializer):

    class Meta(BaseSelectionModelSerializer.Meta):
        model = Group


class GroupRelatedUserModelSerializer(BaseRelModelSerializer):
    id = serializers.CharField(source='user_id', read_only=True)
    name = serializers.CharField(source='user__username', read_only=True)
    user_ids = serializers.ListField(
        min_length=1,
        max_length=10,
        write_only=True,
        child=serializers.PrimaryKeyRelatedField(queryset=User.objects.all()))

    class Meta(BaseModelSerializer.Meta):
        model = UserGroupRel
        fields = BaseModelSerializer.Meta.fields + ('user_ids', )
        read_only_fields = BaseModelSerializer.Meta.read_only_fields

    def create(self, validated_data):
        for user in validated_data.pop('user_ids'):
            instance = UserGroupRel.objects.filter(
                    user_id=user.id,
                    group_id=validated_data['group_id']).first()
            if instance is None:
                validated_data['user_id'] = user.id
                instance = super().create(validated_data)
        return instance
