from sqlite3 import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import ToDoForm
from .models import ToDo

# Create your views here.


def home(request):
    return render(request, 'todo/home.html')


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


def logOutUser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def logInUser(request):
    if request.method == 'GET':
        return render(request, 'todo/login.html',{'form':AuthenticationForm()})
    if request.method == "POST":
        user = authenticate(request=request, username=request.POST['username'], password=request.POST['password'])

        if user is None:
            return render(request, 'todo/login.html',{'form':AuthenticationForm(), 'error':"Username and password do not match"})
        else:
            login(request, user)
            return redirect('dashboard')

def dashboard(request):
    todos = ToDo.objects.filter(user = request.user)
    return render(request, 'todo/dashboard.html', {'todos':todos})

def createToDos(request):
    if request.method == 'GET':
        return render(request, 'todo/createToDo.html',{'form':ToDoForm()})
    else:
        try:
            form = ToDoForm(request.POST)
            newToDo = form.save(commit=False)
            newToDo.user = request.user
            newToDo.save()
            return redirect('dashboard')
        except ValueError:
            return render(request, 'todo/createToDo.html',{'form':ToDoForm(), 'error':'The value entered is not supported'})