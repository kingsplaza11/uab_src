from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# defining the custom user manager
class AccountManager(BaseUserManager):

    def create_user(self, email, username, password=None, **other_fields):
        if not email:
            raise ValueError('Please provide an email address')
        if not username:
            raise ValueError('Please fill in a username')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **other_fields):
        user = self.create_user(
            email = self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

#define custom User model
class Account(AbstractBaseUser, PermissionsMixin):
    email                    = models.EmailField(verbose_name='email address', unique=True, max_length=255)
    username                 = models.CharField(verbose_name='username', max_length=100, unique=False)
    fullname                 = models.CharField(verbose_name='fullname', max_length=200, unique=False)
    date_joined              = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login               = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_active                = models.BooleanField(default=True)
    is_admin                 = models.BooleanField(default=False)
    is_staff                 = models.BooleanField(default=False)
    is_superuser             = models.BooleanField(default=False)
    phone_number             = models.CharField(max_length=50, blank=True, null=True)
    country                  = models.CharField(max_length=50, blank=True, null=True)
    address                  = models.CharField(max_length=100, blank=True, null=True)
    pass_phrase              = models.CharField(max_length=100, blank=True, null=True, default='elite+sway+random')
    photo                    = models.ImageField(upload_to='profile_photo', null=True, blank=True)
    # ==>
    
    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']   
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True



    


