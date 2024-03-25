# Create your views here.
from drf_spectacular.utils import extend_schema_view, extend_schema
from django.utils.translation import gettext_lazy as _

from rest_framework_admin.user.group import serializers
from rest_framework_admin.user.group.filters import GroupFilter, GroupRelatedUserFilter
from rest_framework_admin.user.group.models import Group, UserGroupRel
from rest_framework_admin.user.group.permissions import GroupModelPermission
from rest_framework_admin.user.group.serializers import GroupModelSerializer
from rest_framework_admin.user.permissions import UserModelPermission
from rest_framework_util.exceptions import HTTP403
from rest_framework_util.viewsets import BaseModeViewSet, BaseRelModelViewSet


@extend_schema_view(
    switch=extend_schema(summary='启用、禁用'),
)
class GroupModelViewSet(BaseModeViewSet):
    """ 组管理 """
    queryset = Group.objects.filter().order_by('-create_datetime').all()
    serializer_class = GroupModelSerializer
    serializer_module = serializers
    filterset_class = GroupFilter
    search_fields = ['id', 'name']
    ordering_fields = ['name', 'create_datetime']
    permission_classes = (GroupModelPermission,)

    def perform_destroy(self, instance):
        if instance.users.exists():
            raise HTTP403(_('存在关联用户，不允许删除'))
        if instance.filter_roles().exists():
            raise HTTP403(_('存在关联角色，不允许删除'))
        instance.delete(delete_user_id=self.request.user.id)


@extend_schema_view()
class GroupRelatedUserModelViewSet(BaseRelModelViewSet):
    """ 组关联的用户管理 """
    parent_model = Group
    lookup_field = 'user_id'
    queryset = UserGroupRel.objects.all()
    serializer_class = serializers.GroupRelatedUserModelSerializer
    filterset_class = GroupRelatedUserFilter
    search_fields = ['user__username', 'user__nickname']
    ordering_fields = [
        'create_datetime',
        'user__username',
        'user__create_datetime']
    ordering = ['-create_datetime']
    permission_classes = (UserModelPermission,)
