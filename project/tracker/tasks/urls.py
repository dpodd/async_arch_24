from django.urls import path

from .views import home, create_task, reassign_tasks, my_tasks_dashboard, complete_tasks


urlpatterns = [
    path('', home, name='home'),
    path('tasks/create/', create_task, name='create_task'),
    path('tasks/reassign/', reassign_tasks, name='reassign_tasks'),
    path('tasks/my_tasks/', my_tasks_dashboard, name='my_tasks'),
    path('tasks/complete_tasks/', complete_tasks, name='complete_tasks'),
]