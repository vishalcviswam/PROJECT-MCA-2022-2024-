from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import User, NormalUser, CollegeUser , Department , Course, Instructor

from datetime import date
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404

from django.views.generic import View
from .utils import *

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
    return render(request, 'home.html')

@login_required(login_url='loginnew')
def home2(request):
    return render(request, 'home2.html')

def news(request):
    return render(request,'news.html')

def profile(request):
    return render(request,'profile.html')

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
            user = User(username=uname, email=email, is_normal_user=True)
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
                return redirect('home2')
        else:
            return render(request, 'loginpage.html', {'error_message': 'Username or password is incorrect'})

    return render(request, 'loginpage.html')

@login_required(login_url='loginnew')
def normal_user_home(request):
    return render(request, 'normal_user_home.html')

@login_required(login_url='loginnew')
def college_user_home(request):
    return render(request, 'college_user_home.html')

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


def add_course(request):
    if request.method == 'POST':
        # Retrieve form data
        course_name = request.POST['course_name']
        course_duration = request.POST['course_duration']
        course_fee = request.POST['course_fee']
        course_description = request.POST['course_description']
        languages = request.POST['languages']
        course_level = request.POST['course_level']
        certificate_available = 'certificate_available' in request.POST
        exam = 'exam' in request.POST
        assignment = 'assignment' in request.POST
        course_type = request.POST['course_type']
        instructors = request.POST.getlist('instructors')
        department_id = request.POST['department']

        # Retrieve the current logged-in user
        user = request.user

        # Retrieve the CollegeUser instance associated with the user
        college_user = CollegeUser.objects.get(user=user)

        # Retrieve the department based on the department_id
        try:
            department = Department.objects.get(pk=department_id)
        except Department.DoesNotExist:
            # Handle the case where the department does not exist
            pass

        # Create a new course
        course = Course(
            college=college_user,  # Assign the CollegeUser instance to the course
            department=department,  # Assign the Department instance to the course
            course_name=course_name,
            course_duration=course_duration,
            course_fee=course_fee,
            course_description=course_description,
            languages=languages,
            course_level=course_level,
            certificate_available=certificate_available,
            exam=exam,
            assignment=assignment,
            course_type=course_type,
        )
        course.save()

        # Add selected instructors to the course
        for instructor_id in instructors:
            instructor = Instructor.objects.get(pk=instructor_id)
            course.instructors.add(instructor)

        return redirect('home2')  # Redirect to a page showing all courses

    else:
        instructors = Instructor.objects.all()
        departments = Department.objects.all()  # Add this line to fetch all departments
        return render(request, 'course.html', {'instructors': instructors, 'departments': departments})



