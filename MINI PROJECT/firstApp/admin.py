from django.contrib import admin

from .models import NormalUser, CollegeUser

class NormalUserAdmin(admin.ModelAdmin):
    # Customize the NormalUser admin if needed
    pass

class CollegeUserAdmin(admin.ModelAdmin):
    # Customize the CollegeUser admin if needed
    pass

admin.site.register(NormalUser, NormalUserAdmin)
admin.site.register(CollegeUser, CollegeUserAdmin)