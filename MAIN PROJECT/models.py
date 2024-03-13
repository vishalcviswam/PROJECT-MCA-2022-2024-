import re
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import ValidationError



class User(AbstractUser):
    is_normal_user = models.BooleanField(default=False)
    is_college_user = models.BooleanField(default=False)
    is_content_creator = models.BooleanField(default=False)
    
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

class ContentCreators(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=30,null=True)
    last_name = models.CharField(max_length=30,null=True)
    phone_number = models.CharField(max_length=15, null=True)
    country = models.CharField(max_length=100, null=True)
    gender = models.CharField(max_length=10, null=True)
    profile_photo = models.ImageField(blank=True, null=True, upload_to='creators_profile_photos/')
    cover_photo = models.ImageField(blank=True, null=True, upload_to='creators_cover_photos/')
    about_me = models.TextField(blank=True, null=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username

class Awards(models.Model):
    content_creator = models.ForeignKey(ContentCreators, on_delete=models.CASCADE, related_name='awards')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    date_awarded = models.DateField()

    def __str__(self):
        return f"{self.title} - {self.content_creator.user.username}"

class Documents(models.Model):
    content_creator = models.ForeignKey(ContentCreators, on_delete=models.CASCADE, related_name='documents')
    document = models.FileField(upload_to='content_creator_documents/')
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.description} - {self.content_creator.user.username}"


class Educations(models.Model):
    EDUCATION_LEVEL_CHOICES = [
        ('School', 'School'),
        ('Bachelor', 'Bachelor'),
        ('Master', 'Master'),
    ]

    content_creator = models.ForeignKey(ContentCreators, on_delete=models.CASCADE, related_name='education')
    level = models.CharField(max_length=100, choices=EDUCATION_LEVEL_CHOICES)
    school_name = models.CharField(max_length=255, blank=True, null=True)
    percentage_mark = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    stream = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.level} - {self.school_name} - {self.content_creator.user.username}"

class WorkExperiences(models.Model):
    content_creator = models.ForeignKey(ContentCreators, on_delete=models.CASCADE, related_name='work_experience')
    organization_name = models.CharField(max_length=255)
    years_of_experience = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return f"{self.organization_name} - {self.years_of_experience} years - {self.content_creator.user.username}"


class Department(models.Model):
    college = models.ForeignKey(CollegeUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255,unique=True)
    undergrad_offered = models.BooleanField(default=False)
    postgrad_offered = models.BooleanField(default=False)
    head_of_department = models.CharField(max_length=255)
    department_start_year = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

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
    college = models.ForeignKey(CollegeUser, on_delete=models.CASCADE, null=True, blank=True)
    content_creator = models.ForeignKey(ContentCreators, on_delete=models.CASCADE, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
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
        

class CourseEnrollment(models.Model):
    enrollment_id = models.AutoField(primary_key=True)
    normal_user = models.ForeignKey('NormalUser', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Enrollment {self.enrollment_id}: {self.normal_user.user.username} in {self.course.course_name}"
    

class CourseProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_progress')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_progress')
    reading_progress = models.IntegerField(default=0)
    video_progress = models.IntegerField(default=0)
    quiz_progress = models.IntegerField(default=0)
    # You can add other fields to track different types of progress

    class Meta:
        unique_together = ('user', 'course')  # Ensure one entry per user per course

    def overall_progress(self):
        # Here you can customize how you want to calculate the overall progress
        total = self.reading_progress + self.video_progress + self.quiz_progress
        count = 3  # Total number of components
        return total / count if count else 0

    def __str__(self):
        return f"{self.user.username}'s progress on {self.course.course_name}"
    

class CourseCompletion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_completions')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_completions')
    completed = models.BooleanField(default=False)
    completion_date = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'course')  # Ensure one entry per user per course

    def __str__(self):
        completion_status = 'completed' if self.completed else 'not completed'
        return f"{self.user.username}'s course {self.course.course_name} is {completion_status}"
    


class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    college_user = models.ForeignKey(CollegeUser, on_delete=models.CASCADE, null=True, blank=True)
    content_creator = models.ForeignKey(ContentCreators, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='posts/images/', blank=True, null=True)
    video = models.FileField(upload_to='posts/videos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_posts', blank=True)
    saved_by_users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='SavedPost', related_name='posts_saved')



    def __str__(self):
        return f"Post {self.post_id} by {self.get_author_username()}"
    

    def get_author_username(self):
        if self.college_user:
            return self.college_user.user.username
        elif self.content_creator:
            return self.content_creator.user.username
        else:
            return "Unknown"
    
    @property
    def total_likes(self):
        return self.likes.count()
    
    def get_hashtags(self):
        # Regular expression to extract hashtags
        return re.findall(r"#(\w+)", self.content)

    @staticmethod
    def get_posts_by_hashtag(hashtag):
        # A static method to get posts containing a specific hashtag
        return Post.objects.filter(content__icontains=f'#{hashtag}').distinct()
    
    def get_college_profile_photo_url(self):
        if self.college_user and self.college_user.profile_photo:
            return self.college_user.profile_photo.url
        elif self.content_creator and self.content_creator.profile_photo:
            return self.content_creator.profile_photo.url
        else:
            return 'path/to/default/image'  # You can set a default image path here

    def get_college_name(self):
        if self.college_user:
            return self.college_user.college_name
        elif self.content_creator:
            return self.content_creator.college_name
        else:
            return "Unknown"

    

class Image(models.Model):
    post = models.ForeignKey(Post, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/images/')

class Video(models.Model):
    post = models.ForeignKey(Post, related_name='videos', on_delete=models.CASCADE)
    video = models.FileField(upload_to='posts/videos/')



class SavedPost(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='saved_post_entries'  # Unique related_name for the User -> SavedPost relationship
    )
    post = models.ForeignKey(
        'Post', 
        on_delete=models.CASCADE, 
        related_name='saved_post_entries'  # Unique related_name for the Post -> SavedPost relationship
    )
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')  # This constraint is fine

    def __str__(self):
        return f"{self.user.username} saved Post {self.post.post_id}"
    

class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    progress = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'chapter')

    def __str__(self):
        return f"{self.user.username} - {self.chapter.chapter_name} - {'Completed' if self.progress else 'In Progress'}"



class AudioFile(models.Model):
    audio = models.FileField(upload_to='uploads/')


class Payment(models.Model):
    normal_user = models.ForeignKey('NormalUser', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    razorpay_payment_id = models.CharField(max_length=100)
    razorpay_order_id = models.CharField(max_length=100)
    razorpay_signature = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.normal_user.user.username} - {self.course.course_name} - {self.razorpay_payment_id}"
    


class Community(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    cover_photo = models.ImageField(upload_to='community_covers/', null=True, blank=True)
    profile_photo = models.ImageField(upload_to='community_profiles/', null=True, blank=True)
    rules = models.TextField(blank=True, null=True)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    content_creator = models.ForeignKey('ContentCreators', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.course.course_name}"


class CommunityMembership(models.Model):
    community = models.ForeignKey('Community', on_delete=models.CASCADE, related_name='memberships')
    user = models.ForeignKey('NormalUser', on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.user.username} in {self.community.name}"

class Message(models.Model):
    community = models.ForeignKey('Community', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    posted_at = models.DateTimeField(auto_now_add=True)
    file_attachment = models.FileField(upload_to='message_attachments/', null=True, blank=True)



    def __str__(self):
        return f"Message by {self.user.username} on {self.posted_at.strftime('%Y-%m-%d %H:%M')}"

    

class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Below Average'),
        (3, '3 - Average'),
        (4, '4 - Good'),
        (5, '5 - Excellent'),
    ]

    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    enrollment = models.ForeignKey('CourseEnrollment', on_delete=models.CASCADE, null=True, blank=True)
    rating = models.IntegerField(choices=RATING_CHOICES)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.course.course_name}"
