from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


# Create your models here.
class Account(AbstractBaseUser):

    profile_img = models.TextField()
    nickname = models.CharField(max_length=25, unique=True)
    name = models.CharField(max_length=25)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'nickname'

    class Meta:
        db_table = "User"
