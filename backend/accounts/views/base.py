from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from companies.models import Enterprise
from companies.models import Employee

class Base(APIView):
    def get_enterprise_user(self,user_id):
        enterprise = {
            'isowner' : False,
            'permission': []
        }
        enterprise['isowner'] = Enterprise.objects.filter(user_id=user_id).exists()
        if enterprise['isowner']:return True

        employe = Employee.objects.filter(user_id=user_id).first

        if not employe: raise APIException('Este usuário não existe no banco de dadosd')

        from accounts.models import UserGroups,Group_Permissions
        groups = UserGroups.objects.filter(user_id=user_id).all()

        for g in groups:
            group = g.group
            permission = Group_Permissions.objects.filter(group_id=group.id).all()
            for p in permission:
                enterprise['permission'].append(
                    {'id':p.permission.id,
                    'label':p.permission.name,
                    'codename':p.permission.codename}
                )
        return enterprise