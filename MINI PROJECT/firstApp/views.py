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

        college_user = CollegeUser(user=user, colleg
                                   e_name=cname, address=address, contact_email=email, contact_phone_number=phone)
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
                return redirect('home')
            elif user.is_college_user:
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
