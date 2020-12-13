from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'task/home.html')


def signupuser(request):

    if request.method == 'GET':
        return render(request, 'task/signupuser.html', {'form':UserCreationForm()})

    else:

        if request.POST['password1'] == request.POST['password2']:

            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttask')

            except IntegrityError:
                return render(request, 'task/signupuser.html', {'form': UserCreationForm(), 'error': 'That username already exists. Try a new one!'})

        else:
            return render(request, 'task/signupuser.html', {'form':UserCreationForm(), 'error':'Password did not match!'})


def loginuser(request):

    if request.method == 'GET':
        return render(request, 'task/loginuser.html', {'form':AuthenticationForm()})

    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'task/loginuser.html', {'form': AuthenticationForm(), 'error':'Username and Password did not match!'})
        else:
            login(request, user)
            return redirect('currenttask')


def logoutuser(request):

    if request.method == 'POST':
        logout(request)
        return redirect('home')


@login_required
def createtask(request):
    if request.method == 'GET':
        return render(request, 'task/createtask.html', {'form':TaskForm()})
    else:
        try:
            form = TaskForm(request.POST)
            newtask = form.save(commit=False)
            newtask.user = request.user
            newtask.save()
            return redirect('currenttask')
        except ValueError:
            return render(request, 'task/createtask.html', {'form': TaskForm(), 'error': 'Title is too big. Try a new one!'})


@login_required
def currenttask(request):
    todos = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'task/currenttask.html', {'todos': todos})


@login_required
def completedtask(request):
    todos = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'task/completedtask.html', {'todos': todos})


@login_required
def viewtask(request, todo_pk):
    task = get_object_or_404(Task, pk=todo_pk, user=request.user)
    form = TaskForm(instance=task)
    return render(request, 'task/viewtask.html', {'task': task, 'form':form})


@login_required
def edittask(request, todo_pk):
    task = get_object_or_404(Task, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TaskForm(instance=task)
        return render(request, 'task/edittask.html', {'task': task, 'form': form})
    else:
        try:
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('currenttask')
        except ValueError:
            return render(request, 'task/edittask.html', {'task': task, 'form': form, 'error': 'Title is too big. Try a new one!'})


@login_required
def completetask(request, todo_pk):
    task = get_object_or_404(Task, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('currenttask')


@login_required
def deletetask(request, todo_pk):
    task = get_object_or_404(Task, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('currenttask')
