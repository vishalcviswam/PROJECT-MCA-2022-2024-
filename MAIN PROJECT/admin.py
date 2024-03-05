from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, NormalUser, CollegeUser ,Department ,Course, Instructor , VideoMaterial , Post , CourseEnrollment ,ContentCreators , Community

# Define a custom UserAdmin class that inherits from the base UserAdmin
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'is_normal_user', 'is_college_user','is_content_creator',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_staff=False)  # Exclude staff members

# Register the User model with the custom admin class
admin.site.register(User, CustomUserAdmin)

# Register the NormalUser and CollegeUser models
admin.site.register(NormalUser)
admin.site.register(CollegeUser)
admin.site.register(ContentCreators)
admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Instructor)
admin.site.register(VideoMaterial)
admin.site.register(Post)
admin.site.register(Community)
admin.site.register(CourseEnrollment)

