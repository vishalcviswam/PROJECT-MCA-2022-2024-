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


@login_required(login_url='login_view')
def home(request):
    return render (request,'home.html')

# Create your views here.

def your_view(request):
    today_date = date.today().isoformat()
    return render(request, 'registerpage.html', {'today_date': today_date})

def registernew(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        uname = request.POST.get('uname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        print("Received uname:", uname)

        if password != cpassword:
            return HttpResponse("Your password and confirm password do not match!")

        try:
            # Create a User instance and set the necessary attributes
            newuser = User.objects.create_user(username=uname, email=email, password=password)
            newuser.first_name = name  # Set the first_name attribute
            newuser.save()
            return redirect('login_view')
        except IntegrityError:
            return HttpResponse("Username already exists. Please choose a different username.")
    
    return render(request, 'registerpage.html')


def login_view(request):
    if request.method == 'POST':
        usename = request.POST['usename']
        passname = request.POST['passname']

        user = authenticate(request, username=usename, password=passname)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'loginpage.html', {'error_message': 'Username or password is incorrect'})

    return render(request, 'loginpage.html')


def logoutp(request):
    logout(request)
    return redirect('login_view')