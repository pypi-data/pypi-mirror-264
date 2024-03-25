#!/usr/bin/python
# -*- coding:utf-8 -*-
# Email:iamfengdy@126.com
# DateTime:2024/1/2
# Tool:PyCharm

"""  """
__version__ = '0.0.1'
__history__ = """"""
__all__ = []
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.generics import RetrieveAPIView, CreateAPIView

from rest_framework_admin.auth.serializers import AuthMeUserModelSerializer, RegisterUserModelSerializer


@extend_schema_view(
    get=extend_schema(summary='用户自查')
)
class AuthMeRetrieveAPIView(RetrieveAPIView):
    serializer_class = AuthMeUserModelSerializer

    def get_object(self):
        return self.request.user


@extend_schema_view(
    post=extend_schema(summary='用户注册')
)
class AuthRegisterCreateAPIView(CreateAPIView):
    serializer_class = RegisterUserModelSerializer
