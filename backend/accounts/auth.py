from rest_framework.exceptions import AuthenticationFailed, APIException
from accounts.models import User
from django.contrib.auth.hashers import check_password, make_password
from companies.models import Enterprise
from companies.models import Employee


class Authentication:
    def sigin(self, email=None, password=None) -> User:
        user_exist = User.objects.filter(email=email).exists()

        if not user_exist:
            raise AuthenticationFailed(
                f'Email ({email}) incorreto ou não existente')

        user = User.objects.filter(email=email).first()

        if not check_password(password, user.password):
            raise AuthenticationFailed(
                f'Senha errada para o email {email}')

        return user

    def signup(self, name, email, password, type_account='owner', company_id=False):
        if not name or name == "":
            raise APIException(
                'O nome não deve ser nulo')
        if not email or email == "":
            raise APIException('O email não deve ser nulo')
        if not password or password == "":
            raise APIException('O password não deve ser nulo')
        if type_account == 'employee' and not company_id:
            raise APIException('O id da empresa não deve ser nulo')

        user = User

        if user.objects.filter(email=email).exists():
            raise APIException('O email já existe')

        password_hashed = make_password(password)

        created_user = user.objects.create(
            name=name,
            email=email,
            password=password_hashed,
            isowner=1 if type_account == 'owner' else 0
        )

        if type_account == 'owner':
            created_enterprise = Enterprise.objects.create(
                name=f'Empresa de {name}',
                user_id=created_user.id
            )

        if type_account == 'employee':
            Employee.objects.create(
                enterprise_id=company_id or created_enterprise.id,
                user_id=created_user.id
            )

        return created_user
