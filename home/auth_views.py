from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.conf import settings
import jwt
import datetime

def generate_jwt_token(user):
    payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow()
    }
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm='HS256')
    return token

def signup_view(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if pass1 != pass2:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('signup')
            
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect('signup')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()

        messages.success(request, "Your account has been successfully created. Please Login!")
        return redirect('login')

    return render(request, 'home/signup.html')

def login_view(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpass = request.POST['loginpassword']

        user = authenticate(username=loginusername, password=loginpass)

        if user is not None:
            login(request, user)
            
            # JWT Logic
            token = generate_jwt_token(user)
            
            response = redirect('home')
            response.set_cookie(
                'access_token', 
                token, 
                httponly=True, 
                max_age=60*60*24*7, # 7 days
                secure=not settings.DEBUG, # Secure in production
                samesite='Lax'
            )
            
            messages.success(request, "Successfully logged in!")
            return response
        else:
            messages.error(request, "Invalid Credentials, Please try again")
            return redirect('login')

    return render(request, 'home/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    response = redirect('home')
    response.delete_cookie('access_token')
    return response
