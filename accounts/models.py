# from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

# for creating user 
class AccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password = None):
        if not email:
            raise ValueError('Email field is * mandatory for user')
        
        if not username:
            raise ValueError('Username field is * mandatory for user')
        
        user = self.model(
        # normalize_email is used here for making small letters if any 1 enters capital email
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password)
        user.save(using = self._db)
        return user
    
    # creating super user 
    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using = self._db)
        return user
        

# Multiple User Authentication 
class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=40)
    username = models.CharField(max_length=60, unique=True)
    email = models.CharField(max_length=100, unique=True)
    phone_no = models.CharField(max_length=12)

    # Records of User
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    # setup email for login of admin 
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = AccountManager()

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True


