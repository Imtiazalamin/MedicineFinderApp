from django.contrib import admin
from .models import CustomUserRegister

@admin.register(CustomUserRegister)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'user_type']
