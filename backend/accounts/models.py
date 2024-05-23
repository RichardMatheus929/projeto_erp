from django.db import models
from django.contrib.auth.models import AbstractBaseUser,Permission
from companies.models import Enterprise

# Create your models here.
class User(AbstractBaseUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    isowner = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    def __str__(self) -> str:
        return self.email
    
class Group(models.Model):
    name = models.CharField(max_length=100)
    empresa = models.ForeignKey(Enterprise,on_delete=models.CASCADE)

class Group_Permissions(models.Model):
    group = models.ForeignKey(Group,on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission,on_delete=models.CASCADE)

class UserGroups(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    group = models.ForeignKey(Group,on_delete=models.CASCADE)