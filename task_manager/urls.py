from django.urls import path

from .views import task_list_create, task_detail, task_stats

urlpatterns = [
    path('', task_list_create, name='task_list_create'),
    path('<int:pk>/', task_detail, name='task_detail'),
    path('stats/', task_stats, name='task_stats'),
]