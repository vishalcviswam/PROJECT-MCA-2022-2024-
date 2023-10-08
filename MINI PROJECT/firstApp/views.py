from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import User, NormalUser, CollegeUser
from datetime import date

@login_required(login_url='loginnew')
def home(request):
    return render(request, 'home.html')

def your_view(request):
    today_date = date.today().isoformat()
    return render(request, 'registerpage.html', {'today_date': today_date})

def logoutp(request):
    logout(request)
    return redirect('loginnew')

def register_normal_user(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        uname = request.POST['uname']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        if User.objects.filter(username=uname).exists():
            return render(request, 'normal_registerpage.html', {'error_message': 'Username already taken'})

        user = User(username=uname, email=email, is_normal_user=True)
        user.set_password(password)
        user.save()

        normal_user = NormalUser(user=user, phone_number=phone, first_name=fname, last_name=lname)
        normal_user.save()

        return redirect('loginnew')

    return render(request, 'normal_registerpage.html')

def register_college_user(request):
    if request.method == 'POST':
        cname = request.POST['cname']
        uname = request.POST['uname']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        if User.objects.filter(username=uname).exists():
            return render(request, 'college_registerpage.html', {'error_message': 'Username already taken'})

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
                return redirect('home')
        else:
            return render(request, 'loginpage.html', {'error_message': 'Username or password is incorrect'})

    return render(request, 'loginpage.html')

@login_required(login_url='loginnew')
def normal_user_home(request):
    return render(request, 'normal_user_home.html')

@login_required(login_url='loginnew')
def college_user_home(request):
    return render(request, 'college_user_home.html')

def logoutnew(request):
    logout(request)
    return redirect('loginnew')


@login_required(login_url='loginnew')
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

    return redirect('home')
    


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
            return redirect('home')  # Redirect to the home page or any desired URL after updating the profile
        else:
            messages.error(request, 'User is not authenticated or does not have a related NormalUser instance.')
            return redirect('loginnew')  # Redirect to the login page or any other appropriate page

    return render(request, 'update_profile.html')  # Replace 'update_profile.html' with the actual template name



@login_required(login_url='loginnew')
def view_profile(request):
    # Assuming you have a NormalUser instance associated with the logged-in user
    normal_user = request.user.normaluser

    context = {
        'normal_user': normal_user,
    }

    return render(request, 'viewprofile.html', context)