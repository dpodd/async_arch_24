import random

from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST

from oauth.authentication import oauth2_authentication_required
from users.models import User

from .forms import TaskForm
from .models import Task


@oauth2_authentication_required
def home(request):
    tasks = Task.objects.select_related('assigned_to')
    users = User.objects.all()
    return render(request, 'main.html', {'users': users, 'tasks': tasks})


@oauth2_authentication_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            assignable_users = User.objects.exclude(role__in=['manager', 'administrator'])
            if not assignable_users:
                form.add_error(None, ValidationError("There are no users available to assign the task to."))
            else:
                task = form.save(commit=False)
                task.assigned_to = random.choice(assignable_users)
                task.save()
                return redirect('home')
    else:
        form = TaskForm()
    return render(request, 'create_task.html', {'form': form})


@oauth2_authentication_required
def reassign_tasks(request):
    open_tasks = Task.objects.filter(is_completed=False)
    assignable_users = User.objects.exclude(role__in=['manager', 'administrator'])

    if not assignable_users:
        messages.error(request, "No assignable users found.")
        return redirect('home')

    for task in open_tasks:
        task.assigned_to = random.choice(assignable_users)
        task.save()

    messages.success(request, "Tasks have been reassigned successfully.")
    return redirect('home')


@oauth2_authentication_required
def my_tasks_dashboard(request):
    user_tasks = Task.objects.filter(assigned_to=request.user, is_completed=False)
    return render(request, 'my_tasks_dashboard.html', {'tasks': user_tasks})


@require_POST
@oauth2_authentication_required
def complete_tasks(request):
    task_ids = request.POST.getlist('task_ids')
    Task.objects.filter(id__in=task_ids, assigned_to=request.user).update(is_completed=True)
    return redirect('my_tasks')
