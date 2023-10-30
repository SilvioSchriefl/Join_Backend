from django.contrib import admin
from .models import CustomUser  , Contact, Category, Task

class CustomUserAdmin(admin.ModelAdmin):
    pass

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Contact)
admin.site.register(Category)
admin.site.register(Task)
