from accounts.views.base import Base
from accounts.auth import Authentication
from accounts.serializers import UserSerializers
from rest_framework.response import Response
class Signup(Base):
    def post(self,request):
        name = request.data.get('name')
        emai = request.data.get('email')
        password = request.data.get('password')

        user = Authentication.signup(self,name=name,email=emai,password=password,)

        serializer = UserSerializers(user)

        return Response({
            'user':serializer.data,
            'criado em': user.create_account
        })