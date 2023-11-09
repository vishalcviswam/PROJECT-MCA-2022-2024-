from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import ValidationError



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

class Department(models.Model):
    college = models.ForeignKey(CollegeUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255,unique=True)
    undergrad_offered = models.BooleanField(default=False)
    postgrad_offered = models.BooleanField(default=False)
    head_of_department = models.CharField(max_length=255)
    department_start_year = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name

class Instructor(models.Model):
    college = models.ForeignKey(CollegeUser, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    instructor_name = models.CharField(max_length=255)
    subject_taught = models.CharField(max_length=255,null=True, blank=True)
    qualification = models.CharField(max_length=255,null=True, blank=True)
    profile_photo = models.ImageField(blank=True, null=True, upload_to='profile_photo/')

    def __str__(self):
        return self.instructor_name



class Course(models.Model):
    college = models.ForeignKey(CollegeUser, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=255)
    instructors = models.ManyToManyField(Instructor)
    course_duration = models.PositiveIntegerField()  # Duration in days
    course_fee = models.DecimalField(max_digits=10, decimal_places=2)
    course_description = models.TextField()
    languages = models.CharField(max_length=255, blank=True)
    COURSE_LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('expert', 'Expert'),
    ]
    course_level = models.CharField(max_length=20, choices=COURSE_LEVEL_CHOICES)
    certificate_available = models.BooleanField(default=False)
    exam = models.BooleanField(default=False)
    assignment = models.BooleanField(default=False)
    exam_types = models.CharField(max_length=255, blank=True)
    certificate_criteria = models.TextField(blank=True, null=True)
    total_assignments = models.PositiveIntegerField(blank=True, null=True)
    course_tags = models.CharField(max_length=255, blank=True)
    cover_photo = models.ImageField(upload_to='course_covers/', null=True, blank=True)


    def __str__(self):
        return self.course_name
    
class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    module_id = models.AutoField(primary_key=True)
    module_name = models.CharField(max_length=255)

    def __str__(self):
        return self.module_name
    
class Chapter(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='chapters')
    chapter_id = models.AutoField(primary_key=True)
    chapter_name = models.CharField(max_length=255)

    def __str__(self):
        return self.chapter_name


# For reading sections with text and optional images
class ReadingMaterial(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='reading_materials')
    title = models.CharField(max_length=255)
    text_content = models.TextField()
    images = models.ImageField(upload_to='reading_images', blank=True, null=True)

    def __str__(self):
        return self.title

# For video sections with file upload and transcript
class VideoMaterial(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='video_materials')
    video = models.FileField(upload_to='videos')
    transcript = models.TextField()

    def __str__(self):
        return f"Video for {self.chapter}"

# For fill-in-the-blanks questions
class FillInTheBlankQuestion(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='fill_in_the_blank_questions')
    question_text = models.TextField()
    correct_answers = models.JSONField()

    def __str__(self):
        return self.question_text

# For matching questions
class MatchingQuestion(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='matching_questions')
    question_text = models.TextField()
    pairs = models.JSONField()

    def __str__(self):
        return self.question_text

# For image-based questions
class ImageQuestion(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='image_questions')
    image = models.ImageField(upload_to='question_images')
    question_text = models.TextField()
    choices = models.JSONField()
    correct_answer = models.CharField(max_length=255)

    def __str__(self):
        return self.question_text

# For multiple choice questions
class MultipleChoiceQuestion(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='multiple_choice_questions')
    question_text = models.TextField()
    choice_1 = models.CharField(max_length=200,null=True, blank=True)
    choice_2 = models.CharField(max_length=200,null=True, blank=True)
    choice_3 = models.CharField(max_length=200,null=True, blank=True)
    choice_4 = models.CharField(max_length=200,null=True, blank=True)
    correct_answer = models.CharField(max_length=200, help_text="Enter the correct answer exactly as one of the choices.")

    def __str__(self):
        return self.question_text
    
    def clean(self):
        super().clean()
        # Ensure that the correct answer is one of the choices
        correct_answers = (self.choice_1, self.choice_2, self.choice_3,self.choice_4)
        if self.correct_answer not in correct_answers:
            raise ValidationError({'correct_answer': "Correct answer must be one of the choices."})