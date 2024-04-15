from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Chapter, CollegeUser, ContentCreators, Course, CourseEnrollment, Instructor, Module, NormalUser, Post

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            is_normal_user=True
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class NormalUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = NormalUser
        fields = ('user', 'first_name', 'last_name', 'phone_number', 'country', 'gender', 'profile_photo', 'cover_photo', 'about_me')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        normal_user = NormalUser.objects.create(user=user, **validated_data)
        return normal_user

class CollegeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollegeUser
        fields = ['college_name', 'address', 'website', 'contact_email', 'contact_phone_number', 'college_type']  # Adjust fields as needed

class ContentCreatorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentCreators
        fields = ['first_name', 'last_name', 'phone_number', 'country', 'profile_photo', 'cover_photo', 'about_me', 'registration_date']  # Adjust fields as needed

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ['chapter_id', 'chapter_name']

class ModuleSerializer(serializers.ModelSerializer):
    chapters = ChapterSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = ['module_id', 'module_name', 'chapters']

class InstructorSerializer(serializers.ModelSerializer):
    # Make sure all these fields exist in the Instructor model
    class Meta:
        model = Instructor
        fields = ['id', 'instructor_name', 'subject_taught', 'qualification', 'profile_photo']

# Assuming the related name is 'modules' in the Course model
class CourseSerializerNew(serializers.ModelSerializer):
    college = CollegeUserSerializer()
    content_creator = ContentCreatorsSerializer()
    instructors = InstructorSerializer(many=True, read_only=True)
    modules = ModuleSerializer(source='module_set', many=True, read_only=True)  # change related_name if different

    class Meta:
        model = Course
        fields = [
            'course_id', 'course_name', 'college', 'content_creator', 'department',
            'course_duration', 'course_fee', 'course_description', 'languages',
            'course_level', 'certificate_available', 'exam', 'assignment',
            'exam_types', 'certificate_criteria', 'total_assignments', 'course_tags',
            'cover_photo', 'instructors', 'modules'
        ]

    def get_modules(self, obj):
        modules = obj.module_set.all()  # change to 'modules' if your related_name is different
        return ModuleSerializer(modules, many=True).data
    
    
class CourseSerializer(serializers.ModelSerializer):
    college = CollegeUserSerializer()
    content_creator = ContentCreatorsSerializer()

    class Meta:
        model = Course
        fields = '__all__'

class CourseEnrollmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    normal_user = NormalUserSerializer(read_only=True)

    class Meta:
        model = CourseEnrollment
        fields = ('enrollment_id', 'normal_user', 'course', 'enrollment_date', 'is_active')


class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.SerializerMethodField()
    profile_photo_url = serializers.SerializerMethodField()
    total_likes = serializers.ReadOnlyField()
    image_url = serializers.SerializerMethodField()
    video_url = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'post_id', 'author_username', 'content', 'image_url', 'video_url', 
            'created_at', 'profile_photo_url', 'total_likes'
        ]

    def get_author_username(self, obj):
        return obj.get_author_username()

    def get_profile_photo_url(self, obj):
        request = self.context.get('request')
        if obj.college_user and obj.college_user.profile_photo:
            return request.build_absolute_uri(obj.college_user.profile_photo.url)
        elif obj.content_creator and obj.content_creator.profile_photo:
            return request.build_absolute_uri(obj.content_creator.profile_photo.url)
        return None

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None

    def get_video_url(self, obj):
        request = self.context.get('request')
        if obj.video:
            return request.build_absolute_uri(obj.video.url)
        return None