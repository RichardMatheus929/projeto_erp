from companies.views.base import Base
from companies.utils.permission import EmployeesPermission,Group_Permissions
from companies.models import Employee,Enterprise
from companies.serializers import EmployeeSerializer,EmployeesSerializer
from accounts.auth import Authentication
from accounts.models import User,UserGroups
from rest_framework.views import Response,status
from rest_framework.exceptions import APIException

class Emplyoees(Base):
    permission_classes = [EmployeesPermission]

    def get(self,request):
        enterprise_id = self.get_enterprise_id(request.user.id)
        owner_id = Enterprise.objects.filter(id=enterprise_id).first()['user_id'] 
        employees = Employee.objects.filter(enterprise_id=enterprise_id).exclude(user_id=owner_id).all()
        serializer = EmployeesSerializer(employees,many=True)

        return Response({'employees':serializer.data})
    def post(self,request):
        name = request.data.get('name')
        email = request.data.get('email')
        password = request.data.get('password')

        enterprise_id = self.get_enterprise_id(request.user.id)
        signup_user = Authentication.signup(self,name=name,email=email,password=password,type_account='employee',company_id=enterprise_id)
        if isinstance(signup_user,User):
            return Response({'sucess':True},status=status.HTTP_201_CREATED)
        return Response(signup_user,status.HTTP_400_BAD_REQUEST)
    
class EmployeeDetail(Base):
    permission_classes = [EmployeesPermission]
    def get(self,request,employee_id):
        employee = self.get_employee(employee_id, request.user.id)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)
    def put(self,request,employee_id):
        groups = request.data.get('groups')

        employee = self.get_employee(employee_id,request.user.id)

        name = request.data.get('name') or employee.user.name
        email = request.data.get('email') or employee.user.email

        if email != employee.user.email and User.objects.filter(email=email).exists():
            raise APIException("Esse email já está em uso")
        User.objects.filter(id=employee.user.id).update(
            name=name,
            email=email
        )
        UserGroups.objects.filter(userid=employee.user.id).delete()

        if groups:
            groups = groups.split(',')
            for group in groups:
                self.get_group(group_id=group,enterprise_id=employee.enterprise.id)
                UserGroups.objects.create(
                    group_id=group,
                    user_id=employee.user.id
                )
        return Response({'sucess':True})
    def delete(self,request,employee_id):
        employee = self.get_employee(employee_id,request.user.id)

        check_if_owner = User.objects.filter(id=employee.user.id,isowner=1).exists()

        if check_if_owner:
            raise APIException('Você não pode demitir o dono da empresa')
        employee.delete()
        User.objects.filter(id=employee.user.id).delete()
        return Response({'sucess':True})


        
