from django.urls import path
from companies.views.emplyoees import Emplyoees,EmployeeDetail
from companies.views.permissions import PermissionDetail

urlpatterns = [
    path('employees',Emplyoees.as_view()),
    path('employees/<int:employee_id>',EmployeeDetail.as_view()),

    # endpoints de permissao de grupos
    path('permissions',PermissionDetail.as_view())
]