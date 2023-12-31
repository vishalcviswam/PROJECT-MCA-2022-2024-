from collections import Counter
from io import BytesIO
import os
from django.contrib.auth import authenticate, login, logout,get_user_model
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.shortcuts import get_list_or_404, render, redirect
from .models import CourseCompletion, CourseEnrollment, CourseProgress, FillInTheBlankQuestion, ImageQuestion, MatchingQuestion, Post, Progress, SavedPost, User, NormalUser, CollegeUser , Department , Course, Instructor , Module , Chapter , ReadingMaterial, VideoMaterial, MultipleChoiceQuestion

from datetime import date, timezone
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404
from django.http import FileResponse, Http404, HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms import modelformset_factory
import json
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse
from django.core.mail import send_mail
from reportlab.pdfgen import canvas
from django.views.decorators.http import require_POST

 

from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
from django.db import transaction
from django.views.generic import TemplateView
from django.utils import timezone
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from django.contrib.staticfiles import finders
from reportlab.lib import colors



from django.views.generic import View
from .utils import *
import logging

from.utils import TokenGenerator,generate_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMessage
import threading
import razorpay

@login_required(login_url='loginnew')
def home(request):

    posts = Post.objects.all().order_by('-created_at')
    trending_hashtags = get_trending_hashtagss()

    return render(request, 'userhome.html', {'posts': posts,'trending': trending_hashtags})


@login_required(login_url='loginnew')
def home2(request):
    return render(request, 'home2.html')

def news(request):
    return render(request,'news.html')

@login_required(login_url='loginnew')
def profile(request):
    normal_user = request.user.normaluser

    context = {
        'normal_user': normal_user,
    }

    return render(request, 'newprofile.html', context)

@login_required(login_url='loginnew')
def profile2(request):
    college_user = request.user.collegeuser

    context = {
        'college_user': college_user,
    }

    return render(request, 'collegeprofile.html', context)

'''def department(request):
    return render(request,'department.html')'''

def your_view(request):
    today_date = date.today().isoformat()
    return render(request, 'registerpage.html', {'today_date': today_date})

def logoutp(request):
    logout(request)
    return redirect('loginnew')

def register_normal_user(request):
    error_messages = {}  

    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        uname = request.POST['uname']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        if User.objects.filter(username=uname).exists():
            error_messages['uname'] = 'Username already taken'  # Store username error
        if User.objects.filter(email=email).exists():
            error_messages['email'] = 'Email already taken'  # Store email error

        if not error_messages:  # If there are no errors, proceed with registration
            user = User(username=uname, email=email,  is_normal_user=True)
            user.set_password(password)
            #user.is_active=False  #make the user inactive
            user.save()
            current_site=get_current_site(request)  
            email_subject="Activate your account"
            message=render_to_string('activate.html',{
                   'user':user,
                   'domain':current_site.domain,
                   'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                   'token':generate_token.make_token(user)


            })

            email_message=EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email],)
            EmailThread(email_message).start()
            #messages.info(request,"Active your account by clicking the link send to your email")

            
            normal_user = NormalUser(user=user, phone_number=phone, first_name=fname, last_name=lname)
            normal_user.save()

            return redirect('loginnew')

    return render(request, 'normal_registerpage.html', {'error_messages': error_messages})



def register_college_user(request):

    error_messages = {}
    if request.method == 'POST':
        cname = request.POST['cname']
        uname = request.POST['uname']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        if User.objects.filter(username=uname).exists():
            error_messages['uname'] = 'Username already taken'  # Store username error
        if User.objects.filter(email=email).exists():
            error_messages['email'] = 'Email already taken'  # Store email error

        if not error_messages:
            user = User(username=uname, email=email, is_college_user=True)
            user.set_password(password)
            user.save()

            college_user = CollegeUser(user=user, college_name=cname, address=address, contact_email=email, contact_phone_number=phone)
            college_user.save()

            return redirect('loginnew')

    return render(request, 'college_registerpage.html')

def loginnew(request):
    if request.method == 'POST':
        username = request.POST['usename']
        password = request.POST['passname']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_normal_user:
                messages.success(request, 'You successfully signed in as a normal user.')
                return redirect('home')
            elif user.is_college_user:
                messages.success(request, 'You successfully signed in as a college user.')
                return redirect('college_user_home')
            elif user.is_superuser:
                return redirect('admin_home')
        else:
            return render(request, 'loginpage.html', {'error_message': 'Username or password is incorrect'})

    return render(request, 'loginpage.html')

@login_required(login_url='loginnew')
def normal_user_home(request):
    return render(request, 'normal_user_home.html')

@login_required(login_url='loginnew')
def college_user_home(request):
    # Retrieve posts for GET request, ordered with the newest posts first
    posts = Post.objects.all().order_by('-created_at')
    trending_hashtags = get_trending_hashtags()
    
    # Render the college home template with the posts and trending hashtags context
    return render(request, 'collegehome.html', {
        'posts': posts,
        'trending': trending_hashtags
    })


'''def logoutnew(request):
    logout(request)
    return redirect('loginnew')'''


'''@login_required(login_url='loginnew')
def update_profile(request):
    if request.method == 'POST':
        user = request.user

        if user.is_authenticated and hasattr(user, 'normaluser'):
            normal_user = NormalUser

            # Get the uploaded files and text data
            profile_picture = request.FILES.get('profile_picture')
            cover_photo = request.FILES.get('cover_photo')
            about = request.POST.get('about')

            # Update the user's profile
            if profile_picture:
                normal_user.profile_photo = profile_picture
            if cover_photo:
                normal_user.cover_photo = cover_photo
            if about:
                normal_user.about_me = about
            normal_user.save()

            return redirect('home')  # Replace 'profile_success' with your desired URL or template for success
        else:
            return redirect('home')  # Redirect the user to login if not authenticated

    return redirect('home')'''
    



    

@login_required(login_url='loginnew')
def update_profile(request):

    normal_user = request.user.normaluser

    context = {
                'normal_user': normal_user,
            }
    if request.method == 'POST':
        # Get the currently logged-in user
        user = request.user

        # Ensure that the user is authenticated and has a related NormalUser instance
        if user.is_authenticated and hasattr(user, 'normaluser'):
            normal_user = user.normaluser  # Get the NormalUser instance associated with the user

            # Update the user's profile based on form data
            normal_user.first_name = request.POST.get('first_name')
            normal_user.last_name = request.POST.get('last_name')
            normal_user.phone_number = request.POST.get('phone_number')
            normal_user.country = request.POST.get('country')
            normal_user.gender = request.POST.get('gender')


            # Handle profile photo and cover photo uploads
            profile_photo = request.FILES.get('profile_photo')
            if profile_photo:
                normal_user.profile_photo = profile_photo

            cover_photo = request.FILES.get('cover_photo')
            if cover_photo:
                normal_user.cover_photo = cover_photo

            normal_user.about_me = request.POST.get('about_me')
            
            # Save the updated profile
            normal_user.save()

            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')    
        else:
            messages.error(request, 'User is not authenticated or does not have a related NormalUser instance.')
            return redirect('loginnew')  

    return render(request, 'edituserprofile.html',context)


@login_required(login_url='loginnew')
def update_college_profile(request):

    college_user = request.user.collegeuser

    context = {
                'college_user': college_user,
            }
    if request.method == 'POST':
        # Get the currently logged-in user
        user = request.user

        # Ensure that the user is authenticated and has a related NormalUser instance
        if user.is_authenticated and hasattr(user, 'collegeuser'):
            college_user = user.collegeuser  # Get the NormalUser instance associated with the user

            # Update the user's profile based on form data
            college_user.college_name = request.POST.get('college_name')
            college_user.website = request.POST.get('website')
            college_user.contact_phone_number = request.POST.get('contact_phone_number')
            college_user.address = request.POST.get('address')


            # Handle profile photo and cover photo uploads
            profile_photo = request.FILES.get('profile_photo')
            if profile_photo:
                college_user.profile_photo = profile_photo

            cover_photo = request.FILES.get('cover_photo')
            if cover_photo:
                college_user.cover_photo = cover_photo

            
            
            # Save the updated profile
            college_user.save()

            messages.success(request, 'Profile updated successfully.')
            return redirect('profile2')    
        else:
            messages.error(request, 'User is not authenticated or does not have a related College User instance.')
            return redirect('loginnew')  

    return render(request, 'editcollegeprofile.html',context)



@login_required(login_url='loginnew')
def view_profile(request):
    
    normal_user = request.user.normaluser

    context = {
        'normal_user': normal_user,
    }

    return render(request, 'viewprofile.html', context)


@login_required(login_url='loginnew')
def model_update_profile(request):
    if request.method == 'POST':
        
        user = request.user

        if user.is_authenticated and hasattr(user, 'normaluser'):
            normal_user = user.normaluser  

            profile_photo = request.FILES.get('profile_photo')
            if profile_photo:
                normal_user.profile_photo = profile_photo

            cover_photo = request.FILES.get('cover-photo')
            if cover_photo:
                normal_user.cover_photo = cover_photo

            normal_user.about_me = request.POST.get('about_me')
            
            
            normal_user.save()

            messages.success(request, 'Profile updated successfully.')
            return redirect('home') 
        else:
            messages.error(request, 'User is not authenticated or does not have a related NormalUser instance.')
            return redirect('loginnew')  

    return render(request, 'home.html')  

class EmailThread(threading.Thread):
       def __init__(self, email_message):
              super().__init__()
              self.email_message=email_message
       def run(self):
              self.email_message.send()

class ActivateAccountView(View):
    def get(self,request,uidb64,token):
        try:
            uid=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)
        except Exception as identifier:
            user=None
        if user is not None and generate_token.check_token(user,token):
            user.is_active=True
            user.save()
            messages.info(request,"Account activated sucessfully")
            return redirect('loginnew')
        return render(request,"activatefail.html")
    
    
def college_details(request, pk):
    # Retrieve the college user object using the provided pk
    college_user = get_object_or_404(CollegeUser, pk=pk)
    
    # Get all departments related to the college user
    departments = college_user.department_set.all()
    
    return render(request, 'college_details.html', {'college_user': college_user, 'departments': departments})

@login_required(login_url='loginnew')
def add_department(request):
    if request.method == 'POST':
        college_user = get_object_or_404(CollegeUser, user=request.user)
        name = request.POST['department_name']
        programs = request.POST['offered_programs']
        hod = request.POST['head_of_department']

        # Check if department with same name already exists for this college
        if Department.objects.filter(college=college_user, name=name).exists():
            messages.error(request, f"A department with the name '{name}' already exists.")
            return render(request, 'department.html')

        department = Department()
        department.college = college_user
        department.name = name
        department.head_of_department = hod
        department.is_active = True

        if programs == 'both':
            department.undergrad_offered = True
            department.postgrad_offered = True
        elif programs == 'undergrad':
            department.undergrad_offered = True
        elif programs == 'postgrad':
            department.postgrad_offered = True

        department.save()
        messages.success(request, f"Department '{name}' was successfully created.")
        return redirect('college_details', pk=college_user.pk)
    else:
        return render(request, 'department.html')
    
def deactivate_department(request, department_id):
    department = get_object_or_404(Department, pk=department_id)
    if request.method == 'POST':
        department.is_active = not department.is_active  # This toggles the active state
        department.save()
    return redirect('college_details', pk=request.user.pk)


@login_required(login_url='loginnew')
def add_course(request):
    if not request.user.is_authenticated or not request.user.is_college_user:
        return redirect('loginnew') 
    if request.method == 'POST':
        course_name = request.POST['course_name']
        course_duration = request.POST['course_duration']
        course_fee = request.POST['course_fee']
        course_description = request.POST['course_description']
        selected_languages = request.POST.getlist('languages')
        selected_exam_types = request.POST.getlist('exam_types')
        selected_course_tags = request.POST.getlist('course_tags')
        course_level = request.POST['course_level']
        certificate_available = 'certificate_available' in request.POST
        certificate_criteria = request.POST.get('certificate_criteria', '')
        exam = 'exam' in request.POST
        assignment = 'assignment' in request.POST
        total_assignments_str = request.POST.get('total_assignments', '0')
        total_assignments = int(total_assignments_str) if total_assignments_str.isdigit() else 0
        instructors = request.POST.getlist('instructors')
        department_id = request.POST['department']
        cover_photo = request.FILES.get('cover_photo')

        # Handling the relation with logged in user and department
        user = request.user
        college_user = CollegeUser.objects.get(user=user)
        department = Department.objects.get(pk=department_id)

        # Handling the creation of the course
        course = Course(
            college=college_user,
            department=department,
            course_name=course_name,
            course_duration=course_duration,
            course_fee=course_fee,
            course_description=course_description,
            languages=",".join(selected_languages),
            exam_types=",".join(selected_exam_types),
            course_tags=",".join(selected_course_tags),
            course_level=course_level,
            certificate_available=certificate_available,
            certificate_criteria=certificate_criteria if certificate_available else '',
            exam=exam,
            assignment=assignment,
            total_assignments=total_assignments if assignment else 0,
            cover_photo=cover_photo,
        )
        course.save()

        # Handle many-to-many field for instructors
        course.instructors.set(instructors)

        return redirect('add_modules',course_id=course.course_id)
    else:
        instructors = Instructor.objects.filter(college__user=request.user)
        departments = Department.objects.filter(college__user=request.user, is_active=True)
        
        context = {
            'instructors': instructors,
            'departments': departments,
        }
        
        return render(request, 'course.html', context)
    
@login_required(login_url='loginnew')
def add_instructor(request):
    if not request.user.is_authenticated or not request.user.is_college_user:
        return redirect('loginnew') 

    if request.method == 'POST':
        college = CollegeUser.objects.get(user=request.user)
        department = Department.objects.get(pk=request.POST['department'])
        instructor_name = request.POST['instructor_name']
        subject_taught = request.POST['subject_taught']
        qualification = request.POST['qualification']
        profile_photo = request.FILES.get('profile_photo')

        instructor = Instructor(college=college, department=department, instructor_name=instructor_name,subject_taught=subject_taught,qualification=qualification,profile_photo=profile_photo)
        instructor.save()

        return redirect('view_instructors')  
    departments = Department.objects.filter(college__user=request.user)

    context = {
        'departments': departments
    }

    return render(request, 'add_instructor.html', context)



def get_instructors_for_department(request, department_id):
    instructors = Instructor.objects.filter(department_id=department_id).values('id', 'instructor_name')
    return JsonResponse(list(instructors), safe=False)




def view_instructors(request):
    # Ensure the user is logged in and has a related college user
    if not request.user.is_authenticated:
        return redirect('loginnew')
    try:
        user_college = CollegeUser.objects.get(user=request.user)
    except CollegeUser.DoesNotExist:
        # Handle the case where the college user does not exist
        return HttpResponse('You are not associated with any college.', status=403)

    departments = Department.objects.filter(college=user_college, is_active=True)
    selected_department = request.GET.get('department')

    if selected_department:
        instructors = Instructor.objects.filter(
            department__id=selected_department,
            department__is_active=True,
            college=user_college
        ).select_related('department')
    else:
        instructors = Instructor.objects.filter(
            college=user_college
        ).select_related('department')

    context = {
        'departments': departments,
        'instructors': instructors,
        'selected_department': int(selected_department) if selected_department else None
    }
    return render(request, 'view_instructors.html', context)



@login_required
def add_modules(request, course_id):
    course = get_object_or_404(Course, course_id=course_id)
    
    if request.method == 'POST':
        module_names = request.POST.getlist('module_names[]')
        
        for name in module_names:
            Module.objects.create(course=course, module_name=name)
        
        return redirect('add_chapters',course_id=course.course_id)  

    return render(request, 'add_modules.html', {'course': course})


def add_chapters(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    modules = course.module_set.all()  

    if request.method == 'POST':

        module_ids = request.POST.getlist('module_ids[]')
        num_chapters_list = request.POST.getlist('num_chapters[]')

        for index, module_id in enumerate(module_ids):
            num_chapters = int(num_chapters_list[index])
            chapter_names = request.POST.getlist(f'chapter_names_{module_id}[]')

            if num_chapters == len(chapter_names):
                module = get_object_or_404(Module, pk=module_id)
                
                for name in chapter_names:
                    Chapter.objects.create(module=module, chapter_name=name)
            else:
                return JsonResponse({'status': 'error', 'message': 'Chapter count mismatch.'})

        return redirect('add_course_material', course_id=course_id)

    else:
        return render(request, 'add_chapters.html', {'course': course, 'modules': modules})
    

class AddCourseMaterialView(TemplateView):
    template_name = 'add_material.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = get_object_or_404(Course, pk=self.kwargs['course_id'])
        context['modules'] = Module.objects.filter(course=context['course'])
        return context
    

def add_course_material(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    completed_modules = request.session.get('completed_modules', [])

    modules = Module.objects.filter(course=course).exclude(module_id__in=completed_modules)

    if request.method == 'POST':
        print(request.POST)
        print(request.FILES)

        module_id = request.POST.get('module_id')
        module = get_object_or_404(Module, module_id=module_id)
        chapters = module.chapters.all()

        for chapter in chapters:
            material_type_key = f'material_type_{chapter.chapter_id}'
            material_type = request.POST.get(material_type_key)
            print(f"Chapter ID: {chapter.chapter_id}, Material Type: {material_type}")

            if not material_type:
                print(f"No material type provided for chapter ID {chapter.chapter_id}")
                continue

            try:
                if material_type == 'reading':
                    title_key = f'reading_title_{chapter.chapter_id}'
                    text_content_key = f'reading_text_content_{chapter.chapter_id}'
                    image_key = f'reading_images_{chapter.chapter_id}'

                    title = request.POST.get(title_key)
                    text_content = request.POST.get(text_content_key)
                    images = request.FILES.get(image_key) if image_key in request.FILES else None

                    ReadingMaterial.objects.create(
                        chapter=chapter,
                        title=title,
                        text_content=text_content,
                        images=images
                    )
                    print(f"Reading material created for Chapter ID: {chapter.chapter_id}")

                elif material_type == 'video':
                    video_key = f'video_video_{chapter.chapter_id}'
                    transcript_key = f'video_transcript_{chapter.chapter_id}'

                    video = request.FILES.get(video_key)
                    transcript = request.POST.get(transcript_key)

                    VideoMaterial.objects.create(
                        chapter=chapter,
                        video=video,
                        transcript=transcript
                    )
                    print(f"Video material created for Chapter ID: {chapter.chapter_id}")

                elif material_type == 'multiple_choice':
                    # Process each multiple choice question
                    question_keys = [key for key in request.POST if key.startswith(f'mc_question_text_{chapter.chapter_id}')]

                    for question_key in question_keys:
                        # Extracting the index using string manipulation
                        question_index = question_key.split('[')[-1].rstrip(']')

                        # Constructing the keys for choices and the correct answer
                        choices_keys = [
                            f'mc_choice_1_{chapter.chapter_id}[{question_index}]',
                            f'mc_choice_2_{chapter.chapter_id}[{question_index}]',
                            f'mc_choice_3_{chapter.chapter_id}[{question_index}]',
                            f'mc_choice_4_{chapter.chapter_id}[{question_index}]'
                        ]

                        # Retrieving the values for choices and the correct answer
                        choices_values = [request.POST.get(key, '') for key in choices_keys]
                        correct_answer_key = f'mc_correct_answer_{chapter.chapter_id}[{question_index}]'
                        correct_answer_value = request.POST.get(correct_answer_key, '')

                        # Creating the MultipleChoiceQuestion object
                        MultipleChoiceQuestion.objects.create(
                            chapter=chapter,
                            question_text=request.POST[question_key],
                            choice_1=choices_values[0],
                            choice_2=choices_values[1],
                            choice_3=choices_values[2],
                            choice_4=choices_values[3],
                            correct_answer=correct_answer_value
                        )
                        print(f"Multiple choice question {question_index} created for Chapter ID: {chapter.chapter_id}")
                # ... additional elif clauses for other material types ...

            except ValidationError as e:
                print(f"Validation Error for chapter {chapter.chapter_id}: {e}")
                return HttpResponse(f"Validation error: {e}", status=400)
            except json.JSONDecodeError:
                print("Invalid JSON format for answers or pairs")
                return HttpResponse("Invalid JSON format for answers or pairs", status=400)
            
        completed_modules.append(module_id)
        request.session['completed_modules'] = completed_modules
        request.session.modified = True
            
        next_module = modules.exclude(module_id__in=completed_modules).first()
            
        messages.success(request, f"Materials for module '{module.module_name}' saved successfully.")


        if next_module:
            messages.info(request, f"Do you want to add materials to the next module: '{next_module.module_name}'?")
            redirect_url = f"{reverse('add_course_material', args=[course_id])}?module_id={next_module.module_id}"
        else:
            redirect_url = reverse('course_list_college')

        return HttpResponseRedirect(redirect_url)
    

    # If the request method is GET, display the form
    return render(request, 'add_material.html', {'course_id': course_id, 'modules': modules})

def get_next_module(current_module):
    """
    Gets the next module in the course after the current module.

    Args:
    - current_module: The current Module object.

    Returns:
    - The next Module object or None if there is no next module.
    """
    next_modules = Module.objects.filter(
        course=current_module.course, 
        module_id__gt=current_module.module_id
    ).order_by('module_id')
    return next_modules.first()

def get_chapters_for_module(request, module_id):
    # Check for AJAX request header
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        chapters = list(Chapter.objects.filter(module_id=module_id).values('chapter_id', 'chapter_name'))
        return JsonResponse(chapters, safe=False)
    else:
        return HttpResponseBadRequest("This endpoint only accepts AJAX requests.")
    

def course_list(request):
    # Fetch all courses from the database
    courses = Course.objects.select_related('college').all()
    # Render the courses.html template with the courses data
    return render(request, 'courseviewforuser.html', {'courses': courses})


@login_required
def course_list_college(request):
    try:
        college_user = request.user.collegeuser
    except CollegeUser.DoesNotExist:
        college_user = None
    
    if college_user:
        courses = Course.objects.filter(college=college_user)
    else:
        courses = Course.objects.none()

    return render(request, 'courseview.html', {'courses': courses})


def course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    context = {
        'course': course,
    }

    return render(request, 'coursedetails.html', context)


def course_detail_user(request, course_id):
    # Retrieve the Course object by id
    course = get_object_or_404(Course, course_id=course_id)
    # No need to separately retrieve modules or chapters, they can be accessed via the course object in the template

    # Context dictionary to pass data to the template
    context = {
        'course': course,
    }

    # Render the course detail template with the course and related data
    return render(request, 'coursedetailsforusers.html', context)


def chapter_detail(request, chapter_id):
    chapter = get_object_or_404(Chapter, pk=chapter_id)
    context = {
        'chapter': chapter,
    }
    return render(request, 'chapter_detail.html', context)



@login_required
@user_passes_test(lambda u: u.is_staff, login_url='loginnew')
def toggle_user_activation(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    reason = request.POST.get('reason', '')  # Get the reason from POST data

    # If toggling from active to inactive, send an email
    if user.is_active and reason:
        email_subject = 'Your account has been deactivated'
        email_body = f'Your account on our site has been deactivated for the following reason:\n{reason}'
        send_mail(
            email_subject,
            email_body,
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
    
    # If toggling from inactive to active, send an activation email
    elif not user.is_active:
        email_subject = 'Your account has been activated'
        email_body = 'Your account on our site has been activated. You can now login and start using our services.'
        send_mail(
            email_subject,
            email_body,
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )

    user.is_active = not user.is_active
    user.save()
    
    return redirect(reverse('admin_home'))

@login_required(login_url='loginnew')
@user_passes_test(lambda u: u.is_staff, login_url='loginnew')
def admin_home(request):
    # Exclude superusers from the query
    users = User.objects.filter(is_superuser=False)
    return render(request, 'admin.html', {'users': users})




def course_detail_view(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    modules = Module.objects.filter(course=course).prefetch_related('chapters')
    context = {
        'course': course,
        'modules': modules,
    }
    return render(request, 'course_detail.html', context)

logger = logging.getLogger(__name__)

def course_detail_view(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    modules = Module.objects.filter(course=course).prefetch_related('chapters')
    context = {
        'course': course,
        'modules': modules,
        # Add any other context variables that you need to pass to the template
    }
    return render(request, 'course_detail.html', context)





@login_required
def enroll_in_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # AJAX POST request logic here
        data = json.loads(request.body)
        payment_id = data.get('razorpay_payment_id')
        razorpay_order_id = data.get('razorpay_order_id')
        signature = data.get('razorpay_signature')

        try:
            # Verify the payment
            client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            })

            # Payment verification successful
            normal_user, _ = NormalUser.objects.get_or_create(user=request.user)
            enrollment, created = CourseEnrollment.objects.get_or_create(
                normal_user=normal_user, course=course
            )

            # Prepare the message for the response
            if created:
                message = "You have been successfully enrolled in the course."
            else:
                message = "You are already enrolled in this course."

            # Return a JsonResponse with the status and message
            return JsonResponse({'payment_verified': True, 'message': message})

        except razorpay.errors.SignatureVerificationError as e:
            return JsonResponse({'payment_verified': False, 'message': "Payment verification failed."})

        except Exception as e:
            return JsonResponse({'payment_verified': False, 'message': "Error processing payment."})

    elif request.method == 'GET':
        # GET request logic for creating a Razorpay order
        order_amount = int(course.course_fee * 100)  # Convert to paisa
        order_currency = 'INR'
        order_receipt = f'order_rcptid_{course_id}'
        data = {
            'amount': order_amount,
            'currency': order_currency,
            'receipt': order_receipt,
            'payment_capture': '1'
        }

        try:
            razorpay_order = client.order.create(data=data)
            context = {
                'course': course,
                'razorpay_order_id': razorpay_order['id'],
                'razorpay_merchant_key': settings.RAZORPAY_KEY_ID,
                'amount_in_paisa': order_amount
            }
            return render(request, 'coursedetailsforusers.html', context)
        except Exception as e:
            messages.error(request, "Failed to initiate payment process.")
            return HttpResponseRedirect(reverse('course_detail_view', args=[course_id]))
def get_chapter_content(request, chapter_id):
    chapter = get_object_or_404(Chapter, pk=chapter_id)
    reading_materials = chapter.reading_materials.all()
    video_materials = chapter.video_materials.all()
    mcqs = chapter.multiple_choice_questions.all()

    # Since you have separate templates for each type of material, you will render each to a string
    content_html = {
        'reading_materials_html': render_to_string('reading_materials_template.html', {'reading_materials': reading_materials}),
        'video_materials_html': render_to_string('video_materials_template.html', {'video_materials': video_materials}),
        'mcq_html': render_to_string('mcq_template.html', {'mcqs': mcqs}),
    }
    return JsonResponse(content_html)



@login_required
def course_progress(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    course_modules = course.module_set.prefetch_related('chapters').all()
    all_modules_completed = True  # Assume all modules are completed initially

    for module in course_modules:
        chapters = module.chapters.all()
        num_chapters = chapters.count()
        num_completed = Progress.objects.filter(
            user=request.user,
            chapter__in=chapters,
            progress=True
        ).count()
        module.progress_percentage = (num_completed / num_chapters) * 100 if num_chapters else 0
        # If any module is not fully completed, set all_modules_completed to False
        if module.progress_percentage < 100:
            all_modules_completed = False

    return render(request, 'course_progress.html', {
        'course': course,
        'course_modules': course_modules,
        'all_modules_completed': all_modules_completed,
        'course_id': course_id

    })



@login_required
@require_POST
def update_progress(request):
    user = request.user
    chapter_id = request.POST.get('chapter_id')
    completed = request.POST.get('completed') == 'true'
    
    # Use 'pk' or 'id' instead of 'chapter_id' to get the Chapter instance.
    chapter = get_object_or_404(Chapter, pk=chapter_id)
    progress, created = Progress.objects.update_or_create(
        user=user, chapter=chapter, defaults={'progress': completed}
    )
    return JsonResponse({'status': 'success'})

@login_required
def download_certificate(request, course_id):
    # Get the course instance and user details
    course = get_object_or_404(Course, pk=course_id)
    user = request.user

    # Create a file-like buffer to receive PDF data
    buffer = BytesIO()

    # Create the PDF object, using the buffer as its "file"
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter  # save the dimensions of the page size


    # Draw a gradient background
    p.saveState()
    p.setFillColor(HexColor('#ade8f4'))
    p.rect(0, 0, *letter, stroke=0, fill=1)
    p.restoreState()

    p.saveState()
    p.setFillColor(HexColor('#caf0f8'))
    p.rect(0, letter[1] * 0.5, *letter, stroke=0, fill=1)
    p.restoreState()

    p.saveState()
    p.setFillAlpha(0.2)
    p.rect(0, letter[1] * 0.5, *letter, stroke=0, fill=1)
    p.restoreState()

    # Add a border
    p.setStrokeColor(colors.HexColor("#000000"))
    p.setLineWidth(3)
    p.rect(50, 50, width-100, height-100, stroke=True, fill=False)

    # Add the EDUSPHERE FUSION logo on the top right corner
    logo_path = finders.find('images/esf21.png')
    p.drawInlineImage(logo_path, letter[0] - 150, letter[1] - 100, 100, 50)

    # Draw the title and other text
    p.setFont("Helvetica-Bold", 24)
    p.drawCentredString(letter[0] / 2, letter[1] / 2 + 80, course.course_name)
    p.setFont("Helvetica", 12)
    p.drawCentredString(letter[0] / 2, letter[1] / 2 + 60, course.college.college_name)

    # Description
    description = f"{user.get_full_name()} has completed the {course.course_duration} hrs {course.course_name} offered by {course.college.college_name}."
    p.setFont("Helvetica", 14)
    p.drawCentredString(letter[0] / 2, letter[1] / 2, description)

    # Add "EDUSPHERE FUSION" in small text
    p.setFont("Helvetica", 10)
    p.drawRightString(letter[0] - 60, letter[1] - 50, "EDUSPHERE FUSION")

    # Close the PDF object cleanly, and we're done
    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and write it to the response
    pdf = buffer.getvalue()
    buffer.close()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="certificate.pdf"'
    return response

# This is a mock-up function for PDF generation; you'll need to implement it according to your requirements
def generate_certificate_pdf(user, course):
    # Create a file-like buffer to receive PDF data
    buffer = BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF
    p.drawString(100, 100, f"Certificate of Completion for {course.course_name}")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='certificate.pdf')

# Mock-up function to serve a PDF file; you'll need to implement it according to your requirements
def serve_pdf_file_response(file_path):
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename='certificate.pdf')
    else:
        # Handle the error, maybe return a 404 response or a custom error page
        return HttpResponseNotFound('The requested pdf was not found on our server.')
    

@login_required
def post_list_and_create(request):
    # Handle file upload on POST
    if request.method == 'POST':
        content = request.POST.get('content', '')
        image = request.FILES.get('image') if 'image' in request.FILES else None
        video = request.FILES.get('video') if 'video' in request.FILES else None
        
        # Assuming the user is associated with a CollegeUser
        college_user = request.user.collegeuser
        
        # Create and save the new post instance
        Post.objects.create(
            college_user=college_user,
            content=content,
            image=image,
            video=video,
        )
        return redirect('post_list_and_create')  # Redirect to the same page to display the post list

    # Retrieve posts for GET request
    posts = Post.objects.all().order_by('-created_at')  # Assuming you want to display the newest posts first

    # Render the post list template with the posts context
    return render(request, 'collegehome.html', {'posts': posts})


def post_detail(request, post_id):
    # Retrieve a single post by id
    try:
        post = Post.objects.get(post_id=post_id)
    except Post.DoesNotExist:
        return HttpResponse(status=404)

    # Render the post detail template with the post context
    return render(request, 'collegehome.html', {'post': post})

@login_required
@require_POST
def like_post(request):
    data = json.loads(request.body)
    post_id = data.get('id')
    post = get_object_or_404(Post, pk=post_id)  # Simplified with get_object_or_404

    # Toggle like
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    return JsonResponse({
        'total_likes': post.total_likes,
        'liked': liked
    })


@login_required
@require_POST
def save_post(request):
    data = json.loads(request.body)
    post_id = data.get('id')
    post = get_object_or_404(Post, pk=post_id)

    # Check if the post is already saved by the user
    saved_post, created = SavedPost.objects.get_or_create(user=request.user, post=post)

    if not created:
        # The post was already saved, so we unsave it
        saved_post.delete()
        is_saved = False
    else:
        # The post is now saved
        is_saved = True

    return JsonResponse({'is_saved': is_saved})



@login_required
def view_saved_posts(request):
    # Retrieve all instances of SavedPost for the current user
    saved_posts = SavedPost.objects.filter(user=request.user).order_by('-saved_at')

    # Prepare the posts in a format that the template can easily iterate over
    posts = [saved_post.post for saved_post in saved_posts]

    # Pass the posts to the template
    return render(request, 'saved_posts.html', {'saved_posts': posts})


def get_trending_hashtags():
    all_posts = Post.objects.all()
    
    hashtags_counter = Counter()
    
    for post in all_posts:
        hashtags_in_post = post.get_hashtags()
        hashtags_counter.update(hashtags_in_post)
    
    trending_hashtags = hashtags_counter.most_common(10)
    
    trending_with_details = []
    for hashtag, count in trending_hashtags:
        posts = Post.get_posts_by_hashtag(hashtag)
        if posts.exists():
            post = posts.first()
            trending_with_details.append({
                'hashtag': hashtag,
                'count': count,
                'college_name': post.college_user.college_name,
                'profile_photo_url': post.college_user.profile_photo.url if post.college_user.profile_photo else None
            })
    
    return trending_with_details

def posts_by_hashtag(request, hashtag):
    posts = Post.get_posts_by_hashtag(hashtag)
    return render(request, 'collegehome.html', {'posts': posts, 'hashtag': hashtag})



def get_trending_hashtagss():
    # Get all posts
    all_posts = Post.objects.all()
    
    # Create a counter to hold the hashtags and their counts
    hashtags_counter = Counter()
    
    # Go through all posts and update the counter with hashtags from each post
    for post in all_posts:
        hashtags_in_post = post.get_hashtags()
        hashtags_counter.update(hashtags_in_post)
    
    # Get the most common hashtags - specify the number of top trending hashtags you want
    trending_hashtags = hashtags_counter.most_common(10)
    
    # Include college name and photo in the trending data
    trending_with_details = []
    for hashtag, count in trending_hashtags:
        posts = Post.get_posts_by_hashtag(hashtag)
        if posts.exists():
            post = posts.first()
            trending_with_details.append({
                'hashtag': hashtag,
                'count': count,
                'college_name': post.college_user.college_name,
                'profile_photo_url': post.college_user.profile_photo.url if post.college_user.profile_photo else None
            })
    
    return trending_with_details

# View for displaying posts by hashtag
def posts_by_hashtagg(request, hashtag):
    # Use the model's static method to get posts containing the hashtag
    posts = Post.get_posts_by_hashtag(hashtag)
    # Render the page with the filtered posts and the hashtag
    return render(request, 'userhome.html', {'posts': posts, 'hashtag': hashtag})

