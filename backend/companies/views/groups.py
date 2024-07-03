from companies.views.base import Base
from companies.utils.exceptions import RequiredFields
from companies.utils.permission import GroupsPermissionPermission
from companies.serializers import GroupSerializer

from accounts.models import Group,Group_Permissions

from rest_framework.views import Response
from rest_framework.exceptions import APIException

from django.contrib.auth.models import Permission

import pdb

class Groups(Base):
    permission_classes = [GroupsPermissionPermission]

    def get(self,request):
        enterprise_id = self.get_enterprise_id(request.user.id)
        groups = Group.objects.filter(enterprise_id=enterprise_id).all()

        serializer = GroupSerializer(groups,many=True)

        return Response({'groups':serializer.data})
    
    def post(self,request):
        enterprise_id = self.get_enterprise_id(request.user.id)

        name = request.data.get('name')
        permission = request.data.get('permission')

        if not name or name == "":
            raise RequiredFields
        
        created_group = Group.objects.create(
            name=name,
            enterprise_id=enterprise_id
        )

        if permission:
            permission = list(permission.split(','))

            try:
                for item in permission:
                    permission = Permission.objects.filter(id=item).exists()
                    if not permission:
                        created_group.delete()
                        raise APIException(f'A permissão {item} não existe')
                    if not Group_Permissions.objects.filter(group_id=created_group.id,permission_id=item).exists():
                        Group_Permissions.objects.create(
                            group_id=created_group.id,
                            permission_id=item
                        )
            except:
                created_group.delete()
                raise APIException("Permissões no padrão incorreto")
            
        return Response({'sucess':True})

class GroupDetail(Base):
    permission_classes = [GroupsPermissionPermission]

    def get(self,request,group_id):
        enterprise_id = self.get_enterprise_id(request.user.id)

        self.get_group(group_id,enterprise_id)
        group = Group.objects.filter(id=group_id).first()

        serializer = GroupSerializer(group)

        return Response({'group':serializer.data})

    def put(self,request,group_id):
        
        enterprise_id = self.get_enterprise_id(request.user.id)
        self.get_group(group_id,enterprise_id)

        name = request.data.get('name')
        permission = request.data.get('permission')

        Group.objects.filter(id=group_id).update(name=name) if name else None

        Group_Permissions.objects.filter(group_id=group_id).delete()

        if permission:
            permission = list(permission.split(','))
            try:
                for item in permission:
                    permission = Permission.objects.filter(id=item).exists()
                    if not permission:
                        raise APIException(f'A permissão {item} não existe')
                    if not Group_Permissions.objects.filter(group_id=group_id,permission_id=item).exists():
                        Group_Permissions.objects.create(permission_id=item,group_id=group_id)
            except:
                raise APIException("Permissões no padrão incorreto")
        return Response({'sucess':True})
    
    def delete(self,request,group_id):
        enterprise_id = self.get_enterprise_id(request.user.id)

        Group.objects.filter(id=group_id,enterprise_id=enterprise_id).delete()

        return Response({'sucess':True})