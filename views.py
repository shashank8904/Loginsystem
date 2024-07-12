from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

def home(request):
    return render(request, "auth/index.html")

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        if not username or not email or not pass1 or not pass2:
            messages.error(request, "All fields are required.")
            return render(request, "auth/signup.html")
        
        if pass1 != pass2:
            messages.error(request, "Passwords do not match.")
            return render(request, "auth/signup.html")
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, "auth/signup.html")
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return render(request, "auth/signup.html")

        myuser = User.objects.create_user(username, email, pass1)
        myuser.save()
        messages.success(request, "Your account has been created.")
        return redirect('signin')

    return render(request, "auth/signup.html")

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass2 = request.POST.get('pass2')

        user = authenticate(username=username, password=pass2)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Bad credentials!")
            return redirect('signin')
    return render(request, "auth/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('home')
