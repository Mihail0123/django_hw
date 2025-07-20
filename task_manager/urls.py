from django.urls import path


from .views import (
    task_list_create,
    task_detail,
    task_stats,
    SubTaskListCreateView,
    SubTaskDetailUpdateDeleteView,
)

urlpatterns = [
    path('', task_list_create, name='task-list-create'),
    path('<int:pk>/', task_detail, name='task-detail'),
    path('stats/', task_stats, name='task-stats'),
    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtasks/<int:pk>/', SubTaskDetailUpdateDeleteView.as_view(), name='subtask-detail-update-delete'),
]
