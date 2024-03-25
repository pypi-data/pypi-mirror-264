from django.db.models import F, Value, CharField, Q

# Create your views here.
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets
from rest_framework.generics import ListAPIView

from rest_framework_admin.role.configs import SubjectTypeEnum
from rest_framework_admin.role import serializers
from rest_framework_admin.role.filters import RoleFilter, RoleRelatedPermissionFilter, RoleRelatedSubjectFilter, \
    PermissionFilter
from rest_framework_admin.role.models import Role, RolePermissionRel, RoleSubjectRel, Permission
from rest_framework_admin.role.permissions import RoleModelPermission, RoleRelatedPermissionModelPermission, \
    RoleRelatedSubjectModelPermission, SubjectListPermission, PermissionModelPermission
from rest_framework_admin.role.serializers import PermissionModelSerializer
from rest_framework_admin.user.models import User, Group
from rest_framework_util.exceptions import HTTP403
from rest_framework_util.viewsets import BaseModeViewSet, BaseRelModelViewSet


@extend_schema_view()
class PermissionViewSet(viewsets.ReadOnlyModelViewSet):
    """ 权限 """
    queryset = Permission.objects.filter().order_by('-create_datetime').all()
    serializer_class = PermissionModelSerializer
    filterset_class = PermissionFilter
    search_fields = ['name']
    ordering_fields = ['name', 'create_datetime']
    permission_classes = (PermissionModelPermission, )

    def perform_create(self, serializer):
        serializer.save(create_user_id=self.request.user.id)


@extend_schema_view(
    switch=extend_schema(summary='启用、禁用')
)
class RoleModelViewSet(BaseModeViewSet):
    """ 角色 """
    queryset = Role.objects.filter().order_by('-create_datetime').all()
    serializer_class = serializers.RoleModelSerializer
    serializer_module = serializers
    filterset_class = RoleFilter
    search_fields = ['name', 'code']
    ordering_fields = ['name', 'create_datetime']
    permission_classes = (RoleModelPermission, )

    def perform_destroy(self, instance):
        if instance.subject_rels.exists():
            raise HTTP403('存在关联主体，不允许删除')
        if instance.permissions.exists():
            raise HTTP403('存在关联权限，不允许删除')
        instance.delete(delete_user_id=self.request.user.id)


@extend_schema_view()
class RoleRelatedPermissionModelViewSet(BaseRelModelViewSet):
    """ 角色关联的权限管理 """
    parent_model = Role
    lookup_field = 'permission_id'
    queryset = RolePermissionRel.objects.all()
    serializer_class = serializers.RoleRelatedPermissionModelSerializer
    filterset_class = RoleRelatedPermissionFilter
    search_fields = ['permission__name', 'permission__description']
    ordering_fields = [
        'create_datetime',
        'permission__name',
        'permission__create_datetime']
    ordering = ['-create_datetime']
    permission_classes = (RoleRelatedPermissionModelPermission, )


@extend_schema_view()
class RoleRelatedSubjectModelViewSet(BaseRelModelViewSet):
    """ 角色关联的实体管理 """
    parent_model = Role
    lookup_field = 'subject_id'
    queryset = RoleSubjectRel.objects.all()
    serializer_class = serializers.RoleRelatedPermissionModelSerializer
    filterset_class = RoleRelatedSubjectFilter
    search_fields = []
    ordering_fields = [
        'create_datetime',
        'type']
    ordering = ['-create_datetime']
    permission_classes = (RoleRelatedSubjectModelPermission, )


@extend_schema_view()
class SubjectListAPIView(ListAPIView):
    """ 角色主体列表 """
    serializer_class = serializers.SubjectListSerializer
    filterset_class = None
    search_fields = []
    ordering_fields = ['name', 'type']
    ordering = ['name']
    permission_classes = (SubjectListPermission,)

    def get_queryset(self):
        user_queryset = User.objects.filter(is_active=True).annotate(
            name=F('username')).annotate(type=Value(SubjectTypeEnum.user.name, output_field=CharField(max_length=8)))
        group_queryset = Group.objects.filter(is_active=True).annotate(
            type=Value(
                SubjectTypeEnum.user_group.name,
                output_field=CharField(
                    max_length=8)))
        name = self.request.query_params.get('name', None) or None
        if not name:
            name = self.request.query_params.get('search', None) or None
        if name is not None:
            user_queryset = user_queryset.filter(Q(realname__icontains=name) | Q(
                nickname__icontains=name) | Q(username__icontains=name))
            group_queryset = group_queryset.filter(name__icontains=name)

        keys = [
            'id',
            'is_active',
            'description',
            'create_datetime',
            'name',
            'type']
        user_queryset = user_queryset.values(*keys)
        group_queryset = group_queryset.values(*keys)
        subject_type = self.request.query_params.get('type', None) or None
        if subject_type == SubjectTypeEnum.user.name:
            return user_queryset
        elif subject_type == SubjectTypeEnum.user_group.name:
            return group_queryset
        else:
            queryset = user_queryset.union(
                group_queryset, all=True)
        return queryset
