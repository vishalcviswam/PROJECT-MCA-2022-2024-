from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_normal_user = models.BooleanField(default=False)
    is_college_user = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username

class NormalUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=30,null=True)
    last_name = models.CharField(max_length=30,null=True)
    phone_number = models.CharField(max_length=15, null=True)
    country = models.CharField(max_length=100, null=True)
    gender = models.CharField(max_length=10, null=True)
    profile_photo = models.ImageField(blank=True, null=True, upload_to='profile_photos/')
    cover_photo = models.ImageField(blank=True, null=True, upload_to='cover_photos/')
    about_me = models.TextField(blank=True, null=True)
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
class CollegeUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    COLLEGE_TYPE_CHOICES = [
        (1, 'Community colleges'),
        (2, 'Technical colleges'),
        (3, 'Vocational colleges'),
        (4, 'Public universities'),
        (5, 'Private universities'),
        (6, 'For-profit colleges'),
        (7, 'Liberal arts colleges'),
        (8, 'Art colleges'),
        (9, 'Nursing schools'),
        (10, 'Special interest colleges'),
    ]
    college_name = models.CharField(max_length=255)
    address = models.TextField()
    website = models.URLField()
    contact_email = models.EmailField(max_length=254)
    contact_phone_number = models.CharField(max_length=15)
    college_type = models.IntegerField(choices=COLLEGE_TYPE_CHOICES, null=True)
    profile_photo = models.ImageField(blank=True, null=True, upload_to='college_profile_photos/')
    cover_photo = models.ImageField(blank=True, null=True, upload_to='college_cover_photos/')
    verification = models.CharField(max_length=20, default='Pending')
    admin_notes = models.TextField(blank=True, null=True)
    pdf_copy = models.FileField(blank=True, null=True, upload_to='college_pdf_copies/')

    def __str__(self):
        return self.user.username


