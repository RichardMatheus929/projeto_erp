from accounts.views.signin import Signin
from accounts.views.signup import Signup
from accounts.views.user import Getuser
from django.urls import path
urlpatterns = [
    path('signin', Signin.as_view()),
    path('signup', Signup.as_view()),
    path('User', Getuser.as_view())
]
