# todoapp/views.py
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from todoapp import models
from todoapp.models import TODO
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import IntegrityError


def index(request):
    return render(request, 'index.html')



def register(request):
    if request.method == 'POST':
        uname = request.POST.get('uname', '').strip()
        emailid = request.POST.get('email', '').strip()
        pwd = request.POST.get('pwd', '').strip()

        # Basic validation
        if not uname:
            messages.error(request, "Username is required.")
            return render(request, 'register.html')
        
        if not pwd:
            messages.error(request, "Password is required.")
            return render(request, 'register.html')

        try:
            # Create user
            my_user = User.objects.create_user(username=uname, email=emailid, password=pwd)
            my_user.save()
            messages.success(request, "User registered successfully!")
            return redirect('login')  # or any page you want after registration

        except IntegrityError:
            # Username already exists or some DB constraint error
            messages.error(request, "Username already taken. Please choose a different username.")
            return render(request, 'register.html')

        except ValueError as ve:
            # For any ValueErrors like empty username (shouldn't happen now due to checks)
            messages.error(request, f"Error: {ve}")
            return render(request, 'register.html')

        except Exception as e:
            # Catch any other unexpected errors
            messages.error(request, "An unexpected error occurred. Please try again.")
            # Log the error for debugging (optional)
            print(f"Error during registration: {e}")
            return render(request, 'register.html')

    else:
        # For GET requests just show the registration form
        return render(request, 'register.html')


from django.contrib.auth import authenticate, login  # import stays

def login_view(request):  
    if request.method == 'POST':
        uname = request.POST.get('uname')
        pwd = request.POST.get('pwd')
        user = authenticate(request, username=uname, password=pwd)
        if user is not None:
            login(request, user)  
            return redirect('/todo')
        else:
            return redirect('/login')
    return render(request, 'login.html')

def todo(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            # Ensure the user is authenticated
            if request.user.is_authenticated:
                task = models.TODO(title=title, user=request.user)
                task.save()
            else:
                return redirect('/login')  # Redirect to login if user is not logged in

    # Get tasks for the logged-in user
    if request.user.is_authenticated:
        tasks = models.TODO.objects.filter(user=request.user).order_by('-date')
    else:
        tasks = []

    return render(request, 'todo.html', {'res': tasks})

def edit_task(request, sr):
    task = get_object_or_404(models.TODO, pk=sr, user=request.user)
    
    if request.method == 'POST':
        new_title = request.POST.get('title')
        if new_title:
            task.title = new_title
            task.save()
        return redirect('todo')
    
    return render(request, 'edit.html', {'task': task})

def delete_task(request, sr):
    task = get_object_or_404(models.TODO, pk=sr, user=request.user)
    task.delete()
    return redirect('todo')
