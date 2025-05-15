# todoapp/views.py
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from todoapp import models
from todoapp.models import TODO
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render, redirect, get_object_or_404



def register(request):
    if request.method == 'POST':
     uname = request.POST.get('uname') #inside brackets is the name given in html class
     emailid = request.POST.get('email')
     pwd = request.POST.get('pwd')
     print(uname,emailid,pwd)
     my_user = User.objects.create_user(uname,emailid,pwd)
     my_user.save()
     return redirect ('/login')
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
