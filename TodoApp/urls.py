from django.contrib import admin
from django.urls import path, include
from  .import views
urlpatterns = [
    path('', views.index, name='index'),
    path('task/<int:task_id>/edit/', views.task_edit, name='task_edit'),
    path('task/<int:task_id>/delete/', views.task_delete, name='task_delete'),
]
