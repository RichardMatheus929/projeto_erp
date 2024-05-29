from django.urls import path
from companies.views.emplyoees import Emplyoees,EmployeeDetail

urlpatterns = [
    path('employees',Emplyoees.as_view()),
    path('employees/<int:employee_id>',EmployeeDetail.as_view())
]