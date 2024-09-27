from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, CandidateProfile, EmployerProfile

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'user_type']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(CandidateProfile)
admin.site.register(EmployerProfile)

# Register your models here.
