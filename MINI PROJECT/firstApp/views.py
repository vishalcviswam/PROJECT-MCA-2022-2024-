from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import User, NormalUser, CollegeUser , Department , Course, Instructor , Module , Chapter , ReadingMaterial, VideoMaterial, MultipleChoiceQuestion

from datetime import date
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms import modelformset_factory
import json

from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
from django.db import transaction

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
            user.is_active=False  #make the user inactive
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
            messages.info(request,"Active your account by clicking the link send to your email")

            
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
def admin_home(request):
    return render(request, 'admin.html')

@login_required(login_url='loginnew')
def update_profile(request):
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

    return render(request, 'update_profile.html')  



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

@login_required
def add_department(request):
    if request.method == 'POST':
        college_user = CollegeUser.objects.get(user=request.user)

        name = request.POST['department_name']
        programs = request.POST['offered_programs']
        hod = request.POST['head_of_department']
        start_year = request.POST['department_start_year']

        department = Department()
        department.college = college_user
        department.name = name
        department.head_of_department = hod
        department.department_start_year = start_year

        if programs == 'both':
            department.undergrad_offered = True
            department.postgrad_offered = True
        elif programs == 'undergrad':
            department.undergrad_offered = True
        elif programs == 'postgrad':
            department.postgrad_offered = True

        department.save()

        return redirect('college_details', pk=request.user.pk)

    else:
        return render(request, 'department.html')
    
def delete_department(request, department_id):
    department = get_object_or_404(Department, pk=department_id)
    
    if request.method == 'POST':
        department.delete()
    
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
        instructors = Instructor.objects.all()
        departments = Department.objects.filter(college__user=request.user)
        
        context = {
            'instructors': instructors,
            'departments': departments,
        }
        
        return render(request, 'course.html', context)
    

def add_instructor(request):
    if not request.user.is_authenticated or not request.user.is_college_user:
        return redirect('login') 

    if request.method == 'POST':
        college = CollegeUser.objects.get(user=request.user)
        department = Department.objects.get(pk=request.POST['department'])
        instructor_name = request.POST['instructor_name']

        instructor = Instructor(college=college, department=department, instructor_name=instructor_name)
        instructor.save()

        return redirect('view_instructors')  
    departments = Department.objects.filter(college__user=request.user)

    context = {
        'departments': departments
    }

    return render(request, 'instructors_add.html', context)



def get_instructors_for_department(request, department_id):
    instructors = Instructor.objects.filter(department_id=department_id).values('id', 'instructor_name')
    return JsonResponse(list(instructors), safe=False)




def view_instructors(request):
    departments = Department.objects.all()
    selected_department = request.GET.get('department') # Get the department ID from the URL parameter

    if selected_department:
        instructors = Instructor.objects.filter(department__id=selected_department)
    else:
        instructors = Instructor.objects.all()

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

        return redirect('add_material', course_id=course_id)

    else:
        return render(request, 'add_chapters.html', {'course': course, 'modules': modules})
    

@require_http_methods(["POST", "GET"])
def add_material(request, course_id):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                materials_added = []

                # Process each form element for POST request
                for key, value in request.POST.items():
                    if key.startswith('title_'):
                        suffix = key.split('_')[1]
                        material_type = request.POST.get(f'material_type_{suffix}')
                        title = value
                        content = request.POST.get(f'content_{suffix}', '')
                        chapter_id = request.POST.get(f'chapter_id_{suffix}', '')

                        # Ensure we have a valid chapter_id before proceeding
                        if not chapter_id:
                            continue

                        chapter = Chapter.objects.get(pk=chapter_id)

                        if material_type == 'ReadingMaterial':
                            image = request.FILES.get(f'image_{suffix}')  # Adjust the field name if needed
                            if image:
                                material = ReadingMaterial.objects.create(
                                    chapter=chapter,
                                    title=title,
                                    text_content=content,
                                    image=image
                                )
                                materials_added.append(material)

                        elif material_type == 'VideoMaterial':
                            video = request.FILES.get(f'video_{suffix}')  # Adjust the field name if needed
                            if video:
                                material = VideoMaterial.objects.create(
                                    chapter=chapter,
                                    video=video,
                                    transcript=content
                                )
                                materials_added.append(material)

                        elif material_type == 'MultipleChoiceQuestion':
                            question_text = title  # Assuming title is the question text
                            choices = json.loads(request.POST.get(f'choices_{suffix}', '[]'))
                            correct_answer = request.POST.get(f'correct_answer_{suffix}', '')

                            mcq = MultipleChoiceQuestion.objects.create(
                                chapter=chapter,
                                question_text=question_text,
                                choices=json.dumps(choices),
                                correct_answer=correct_answer
                            )
                            materials_added.append(mcq)

                if not materials_added:
                    return HttpResponse('No materials were provided.', status=400)

                return HttpResponse(f'{len(materials_added)} materials added successfully.')

        except Chapter.DoesNotExist:
            return HttpResponse('The specified chapter does not exist.', status=404)
        except json.JSONDecodeError:
            return HttpResponse('Invalid JSON format for choices.', status=400)
        except Exception as e:
            return HttpResponse(f'Unexpected error: {str(e)}', status=500)

    else:  # GET request
        # Logic to handle GET request and display the form
        modules = Module.objects.filter(course_id=course_id).prefetch_related('chapters')
        context = {
            'modules': modules,
            'course_id': course_id
        }
        return render(request, 'add_material.html', context)


    


    



