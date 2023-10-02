from sqlite3 import IntegrityError
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect,render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import date
from django.contrib.auth.hashers import make_password, check_password
from .models import NormalUser, CollegeUser


@login_required(login_url='loginnew')
def home(request):
    return render (request,'home.html')

# Create your views here.

def your_view(request):
    today_date = date.today().isoformat()
    return render(request, 'registerpage.html', {'today_date': today_date})

def logoutp(request):
    logout(request)
    return redirect('loginnew')


def register_normal_user(request):
    if request.method == 'POST':

        fname = request.POST['fname']
        lname=request.POST['lname']
        uname = request.POST['uname']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        if NormalUser.objects.filter(username=uname).exists() or CollegeUser.objects.filter(username=uname).exists():
            return render(request, 'normal_registerpage.html', {'error_message': 'Username already taken'})
            return redirect('register_normal_user')

        # Hash the password
        hashed_password = make_password(password)

        # You can add validation and registration logic here
        normal_user = NormalUser(username=uname, email=email, password=hashed_password)
        normal_user.phone_number = phone
        normal_user.first_name = fname
        normal_user.last_name = lname
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

        if NormalUser.objects.filter(username=uname).exists() or CollegeUser.objects.filter(username=uname).exists():
            return render(request, 'college_registerpage.html', {'error_message': 'Username already taken'})
            return redirect('register_college_user')

        # Hash the password
        hashed_password = make_password(password)

        # You can add validation and registration logic here
        college_user = CollegeUser(username=uname, email=email, password=hashed_password)
        college_user.contact_phone_number = phone
        college_user.college_name = cname
        college_user.address = address
        college_user.save()

        return redirect('loginnew')

    return render(request, 'college_registerpage.html')

def loginnew(request):
    if request.method == 'POST':
        username = request.POST['usename']
        password = request.POST['passname']

        # Authenticate the user
        normal_user = NormalUser.objects.filter(username=username).first()
        college_user = CollegeUser.objects.filter(username=username).first()

        if normal_user and check_password(password, normal_user.password):
            # Redirect to normal user's home page
            return redirect('normal_user_home')
        elif college_user and check_password(password, college_user.password):
            # Redirect to college user's home page
            return redirect('college_user_home')
        else:
            return render(request, 'loginpage.html', {'error_message': 'Username or password is incorrect'})

    return render(request, 'loginpage.html')

def normal_user_home(request):
    return render(request, 'normal_user_home.html')

def college_user_home(request):
    return render(request, 'college_user_home.html')

def logoutnew(request):
    logout(request)
    return redirect('loginnew')