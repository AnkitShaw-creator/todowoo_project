
from sqlite3 import IntegrityError
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
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
            except ValueError:
                return render(request, 'todo/signUp.html',{'form':UserCreationForm(), 'error':'Please enter a valid username and password'})
        else:
            return render(request, 'todo/signUp.html',{'form':UserCreationForm(), 'error':'Password does not match'})


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
    todos = ToDo.objects.filter(user = request.user, datecompleted__isnull=True)
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

def viewToDo(request, todo_pk):
    todo = get_object_or_404(ToDo,pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = ToDoForm(instance=todo)
        return render(request, 'todo/viewToDo.html', {'todo':todo, 'form':form,})
    if request.method == 'POST':
        try:    
            form  = ToDoForm(request.POST, instance=todo)
            form.save()
            return redirect('dashboard')
        except ValueError:
            return render(request, 'todo/viewToDo.html', {'todo':todo, 'form':form,'error': 'Please check the updates made'})



def completeToDo(request, todo_pk):
    todo = get_object_or_404(ToDo,pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.completed = True
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('dashboard')
    #TODO: to be use after removing the completed checkbox from form and model


def deleteToDo(request, todo_pk):
    todo = get_object_or_404(ToDo,pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('dashboard')

def completedToDo(request):
    todos = ToDo.objects.filter(user = request.user, completed=True).order_by('-datecompleted')
    return render(request, 'todo/completedToDo.html', {'todos':todos})