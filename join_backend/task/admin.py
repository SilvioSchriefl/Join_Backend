from django.contrib import admin
from .models import CustomUser  , Contact

class CustomUserAdmin(admin.ModelAdmin):
    pass

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Contact )

