#!/usr/bin/python
# -*- coding:utf-8 -*-
# Email:iamfengdy@126.com
# DateTime:2023/11/17
# Tool:PyCharm

"""  """
__version__ = '0.0.1'
__history__ = """"""

from django.contrib.auth import password_validation
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework.validators import UniqueValidator

from rest_framework_admin.user.models import User, Group, UserGroupRel
from rest_framework_util.serializers import BaseSwitchModelSerializer, BaseModelSerializer, BaseSelectionModelSerializer, BaseRelModelSerializer


class UserModelSerializer(BaseModelSerializer):
    username = serializers.CharField(
        help_text='账户（不允许更新）',
        validators=(
            UniqueValidator(
                queryset=User.objects.filter()),))
    password = serializers.CharField(
        help_text='密码（不允许更新）',
        write_only=True, validators=[
            password_validation.validate_password])
    is_staff = serializers.BooleanField(
        required=False,
        default=True,
        help_text='是否为员工，默认为True')
    is_active = serializers.BooleanField(
        required=False,
        default=True,
        help_text='是否激活，默认为True')
    is_superuser = serializers.BooleanField(
        required=False,
        default=False,
        help_text='是否为超级用户，默认为False')
    description = serializers.CharField(
        required=False, allow_blank=True, allow_null=True, help_text='描述')
    telephone = serializers.CharField(
        required=False, allow_blank=True, allow_null=True, help_text='电话')
    name = serializers.CharField(
        help_text='真实姓名',
        read_only=True)
    nickname = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text='昵称')
    email = serializers.EmailField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text='邮箱')
    # avatar = ImageOrCharField(
    #     max_length=256,
    #     required=False,
    #     allow_blank=True,
    #     allow_null=True)

    class Meta:
        model = User
        read_only_fields = ('create_datetime', 'id', 'last_login')
        exclude = ('delete_user', 'delete_datetime')

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(user.password)
        user.save()
        return user

    def update(self, instance, validated_data):
        validated_data.pop('username', None)
        validated_data.pop('password', None)
        instance = super().update(instance, validated_data)
        return instance


class SwitchUserModelSerializer(BaseSwitchModelSerializer):

    class Meta(BaseSwitchModelSerializer.Meta):
        model = User


class UpdatePasswordUserModelSerializer(serializers.ModelSerializer):
    """ 用户更新密码 """
    old_password = serializers.CharField(help_text='旧密码', write_only=True)
    new_password = serializers.CharField(
        help_text='新密码',
        write_only=True, validators=[
            password_validation.validate_password])

    class Meta:
        model = User
        fields = ('old_password', 'new_password')

    def validate_old_password(self, value):
        if not self.instance.check_password(value):
            raise ValidationError(_('密码错误，请确认'))
        return value

    def update(self, instance, validated_data):
        new_password = validated_data.pop('new_password')
        instance.set_password(new_password)
        instance = super().update(instance, validated_data)
        return instance


class UpdateUserPasswordUserModelSerializer(serializers.ModelSerializer):
    """ 更新用户密码 """
    new_password = serializers.CharField(
        help_text='新密码',
        write_only=True, validators=[
            password_validation.validate_password])

    class Meta:
        model = User
        fields = ('new_password', )

    def update(self, instance, validated_data):
        new_password = validated_data.pop('new_password')
        instance.set_password(new_password)
        instance = super().update(instance, validated_data)
        return instance


class SelectionUserModelSerializer(BaseSelectionModelSerializer):

    class Meta(BaseSelectionModelSerializer.Meta):
        model = User


class UserRelatedGroupModelSerializer(BaseRelModelSerializer):
    id = serializers.CharField(source='group_id', read_only=True)
    name = serializers.CharField(source='group__name', read_only=True)
    group_ids = serializers.ListField(
        min_length=1,
        max_length=10,
        write_only=True,
        child=serializers.PrimaryKeyRelatedField(queryset=Group.objects.all()))

    class Meta(BaseRelModelSerializer.Meta):
        model = UserGroupRel
        fields = BaseRelModelSerializer.Meta.fields + ('group_ids', )

    def create(self, validated_data):
        for group in validated_data.pop('group_ids'):
            if not UserGroupRel.objects.filter(
                    group_id=group.id,
                    user_id=validated_data['user_id']).exists():
                validated_data['group_id'] = group.id
                instance = super().create(validated_data)
        return instance
