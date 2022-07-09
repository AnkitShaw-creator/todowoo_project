from sqlite3 import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login
# Create your views here.


def signUpUser(request):
    if request.method == "GET":
        return render(request, 'todo/signUp.html',{'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('dashboard')
            except IntegrityError:
                return render(request, 'todo/signUp.html',{'form':UserCreationForm(), 'error':'Sorry, that user name is already taken'})
        else:
            return render(request, 'todo/signUp.html',{'form':UserCreationForm(), 'error':'Password is mismatch'})



def dashboard(request):
    return render(request, 'todo/dashboard.html')