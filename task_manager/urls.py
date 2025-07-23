from django.urls import path


from .views import (
    TaskListCreateView,
    TaskDetailView,
    task_stats,
    SubTaskListCreateView,
    SubTaskDetailView,
)

urlpatterns = [
    path('', TaskListCreateView.as_view(), name='task-list-create'),
    path('<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('stats/', task_stats, name='task-stats'),
    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtasks/<int:pk>/', SubTaskDetailView.as_view(), name='subtask-detail-update-delete'),
]
