from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        user = self.create_user(email, password, **extra_fields)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    color = models.CharField(max_length=100, default='#00000', blank=True)
    initials = models.CharField(max_length=100, default='', blank=True)
    user_name = models.CharField(max_length=100, default='', blank=True)
    phone = models.CharField(max_length=100, default='', blank=True)
    contact = models.BooleanField(default=False)
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    
    
class Contact(models.Model):
    email = models.EmailField(unique=True)
    color = models.CharField(max_length=100, default='#00000', blank=True)
    initials = models.CharField(max_length=100, default='', blank=True)
    user_name = models.CharField(max_length=100, default='', blank=True)
    phone = models.CharField(max_length=100, default='', blank=True)
    contact = models.BooleanField(default=True)
    
class Category(models.Model):
    color = models.CharField(max_length=100, default='#00000', blank=True)
    title = models.CharField(max_length=100, default='', blank=True)
    
    
class Task(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default='todo', blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    contacts = models.ManyToManyField(Contact, related_name='tasks', blank=True)
    custom_users = models.ManyToManyField(CustomUser, related_name='collaborator_tasks', blank=True)
    prio = models.CharField(max_length=50)
    subtasks = models.JSONField(default=dict)
    
    
    
    




    
