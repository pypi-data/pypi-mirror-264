# Create your views here.
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.decorators import action
from django.utils.translation import gettext_lazy as _

from rest_framework_admin.user import serializers
from rest_framework_admin.user.filters import UserFilter, UserRelatedGroupFilter
from rest_framework_admin.user.models import User, UserGroupRel
from rest_framework_admin.user.permissions import UserModelPermission, UserRelatedGroupModelPermission
from rest_framework_util.exceptions import HTTP403
from rest_framework_util.viewsets import BaseModeViewSet, BaseRelModelViewSet


@extend_schema_view(
    # list=extend_schema(summary='搜索'),
    # create=extend_schema(summary='增加'),
    # retrieve=extend_schema(summary='查询'),
    # update=extend_schema(summary='全量更新'),
    # partial_update=extend_schema(summary='局部更新'),
    # destroy=extend_schema(summary='删除'),
    switch=extend_schema(summary='启用、禁用'),
    update_password=extend_schema(summary='用户更新密码', description='用户自己更新密码'),
    update_user_password=extend_schema(
        summary='更新用户密码', description='管理员更新指定用户密码'),
)
class UserModelViewSet(BaseModeViewSet):
    """ 用户 """
    queryset = User.objects.all()
    serializer_class = serializers.UserModelSerializer
    serializer_module = serializers
    filterset_class = UserFilter
    search_fields = ['id', 'username', 'nickname', 'realname']
    ordering_fields = ['nickname', 'last_login', 'is_active']
    ordering = ['-create_datetime']
    permission_classes = (UserModelPermission,)

    def perform_destroy(self, instance):
        if instance.groups.exists():
            raise HTTP403(_('存在关联组，不允许删除'))
        # if instance.filter_roles().exists():
        #     raise HTTP403(_('存在关联角色，不允许删除'))
        instance.delete(delete_user_id=self.request.user.id)

    @action(detail=False, methods=['POST'], url_path='password')
    def update_password(self, request, *args, **kwargs):
        """ 用户修改自己的密码 """
        setattr(self, 'get_object', lambda: self.request.user)
        return self.update(request, *args, **kwargs)

    @action(detail=True, methods=['POST'], url_path='password')
    def update_user_password(self, request, *args, **kwargs):
        """ 修改指定用户密码 """
        return self.update(request, *args, **kwargs)


@extend_schema_view()
class UserRelatedGroupModelViewSet(BaseRelModelViewSet):
    """ 用户关联的组管理 """
    parent_model = User
    lookup_field = 'group_id'
    # lookup_url_kwarg = 'pk'
    queryset = UserGroupRel.objects.all()
    serializer_class = serializers.UserRelatedGroupModelSerializer
    filterset_class = UserRelatedGroupFilter
    search_fields = ['group__name', 'group__description']
    ordering_fields = [
        'create_datetime',
        'group__name',
        'group__create_datetime']
    ordering = ['-create_datetime']
    permission_classes = (UserRelatedGroupModelPermission,)
