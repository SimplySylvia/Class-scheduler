from django.shortcuts import render, redirect
# IMPORT DJANGO AUTH
from django.contrib import auth

# IMPORT DJANGO USER MODEL
from django.contrib.auth.models import User

from .forms import ProfileForm

# Create your views here.


def register(request):
    if request.method == 'POST':
        # Get form values
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # Check if passwords match
        if password == password2:
            # Check if username exists
            if User.objects.filter(username=username).exists():
                return render(request, 'register.html', {'error': 'That username has already been registered. Please try a different username'})
            else:
                # Check if email exists
                if User.objects.filter(email=email).exists():
                    return render(request, 'register.html', {'error': 'That email has already been registered'})
                else:
                    # Register User
                    user = User.objects.create_user(
                        username=username, password=password, email=email)
                    user.save()
                    return redirect('login')
        else:
            form = ProfileForm()
            return render(request, 'register.html', {'error': 'Passwords do not match'})
    else:
        form = ProfileForm()
        return render(request, 'register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid Credentials...'})

    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('home')
