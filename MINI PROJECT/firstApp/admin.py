from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, NormalUser, CollegeUser

# Customize the UserAdmin to display your custom fields
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_normal_user', 'is_college_user', 'is_staff')

# Register the User model with the custom admin class
admin.site.register(User, CustomUserAdmin)

# Register the NormalUser and CollegeUser models
admin.site.register(NormalUser)
admin.site.register(CollegeUser)
