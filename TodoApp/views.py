from django.shortcuts import render, redirect, get_object_or_404
from .models import Group, Task
from .forms import GroupForm, TaskForm
from django.http import JsonResponse
from datetime import datetime

def index(request):
    if request.method == 'POST':
        group_name = request.POST.get('grouptask')
        task_description = request.POST.get('task')
        due_date = request.POST.get('due_date')

        # Ensure fields are filled
        if group_name and task_description and due_date:
            group, created = Group.objects.get_or_create(name=group_name)
            Task.objects.create(group=group, description=task_description, due_date=due_date)
            return redirect('index')

    groups = Group.objects.prefetch_related('tasks').all()
    due_tasks = Task.objects.filter(due_date__lt=datetime.now())

    return render(request, 'TodoApp/index.html', {'groups': groups, 'due_tasks': due_tasks})


def task_edit(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        task.description = request.POST['description']
        task.due_date = request.POST['due_date']  # Make sure this is correctly updated
        task.save()
        return redirect('index')

    return render(request, 'TodoApp/task_edit.html', {'task': task})

def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    group = task.group

    task.delete()

    # Delete the group if there are no more tasks
    if not group.tasks.exists():
        group.delete()

    return JsonResponse({'status': 'success'})
