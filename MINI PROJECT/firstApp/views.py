from django.contrib.auth import authenticate, login, logout,get_user_model
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.shortcuts import get_list_or_404, render, redirect
from .models import CourseEnrollment, FillInTheBlankQuestion, ImageQuestion, MatchingQuestion, User, NormalUser, CollegeUser , Department , Course, Instructor , Module , Chapter , ReadingMaterial, VideoMaterial, MultipleChoiceQuestion

from datetime import date
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms import modelformset_factory
import json
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse
from django.core.mail import send_mail

from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
from django.db import transaction
from django.views.generic import TemplateView

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

@login_required(login_url='loginnew')
def home(request):
    return render(request, 'userhome.html')

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
    return render(request, 'collegehome.html')

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
    modules = Module.objects.filter(course=course)

    if request.method == 'POST':
        print(request.POST)
        print(request.FILES)

        module_id = request.POST.get('module_id')
        module = get_object_or_404(Module, pk=module_id)
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
            
        # After successfully creating course material
        messages.success(request, "Course material added successfully!")


        return redirect("course_list_college")

    # If the request method is GET, display the form
    return render(request, 'add_material.html', {'course_id': course_id, 'modules': modules})
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
    course = get_object_or_404(Course, pk=course_id)
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

@login_required
@csrf_exempt  # Only if you're skipping CSRF validation, which is not recommended for production
def enroll_in_course(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, pk=course_id)
        normal_user, created = NormalUser.objects.get_or_create(user=request.user)
        
        enrollment, created = CourseEnrollment.objects.get_or_create(normal_user=normal_user, course=course)
        if created:
            # User was not previously enrolled
            messages.success(request, "You have been successfully enrolled in the course.")
        else:
            # User was already enrolled
            messages.info(request, "You are already enrolled in this course.")
        
        return redirect('course_detail_view', course_id=course_id)

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


