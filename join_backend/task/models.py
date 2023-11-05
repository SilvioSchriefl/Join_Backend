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
    user_contact = models.BooleanField(default=False)
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    
    
class Contact(models.Model):
    email = models.EmailField(unique=True)
    color = models.CharField(max_length=100, default='#00000', blank=True)
    initials = models.CharField(max_length=100, default='', blank=True)
    user_name = models.CharField(max_length=100, default='', blank=True)
    phone = models.CharField(max_length=100, default='', blank=True)
    user_contact = models.BooleanField(default=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,  default=1, blank=True)
    
    def get_title(self):
        return self.user_name
    
class Category(models.Model):
    color = models.CharField(max_length=100, default='#00000', blank=True)
    title = models.CharField(max_length=100, default='', blank=True)
    creator_email = models.EmailField(max_length=70, default='', blank=True)
    
    
    
class Task(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default='todo', blank=True)
    category_title = models.CharField(max_length=50, blank=True)
    category_color = models.CharField(max_length=50, blank=True)
    assigned_emails = models.JSONField(default=dict)
    prio = models.CharField(max_length=50, blank=True)
    subtasks = models.JSONField(default=dict)
    
    
    
    




    
