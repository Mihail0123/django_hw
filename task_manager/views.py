from rest_framework.decorators import api_view, action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.viewsets import ModelViewSet
from django.utils import timezone
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend



from .models import Task, SubTask, Category
from .pagination import SubTaskPagination
from .serializers import TaskSerializer, SubTaskSerializer, CategorySerializer


# Create your views here.

class TaskListCreateView(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']


# Получение конкретной задачи по id
class TaskDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

# Агрегирующий эндпоинт со статистикой задач
@api_view(['GET'])
def task_stats(request):
    total = Task.objects.count()
    by_status = Task.objects.values('status').annotate(count=Count('id'))
    overdue = Task.objects.filter(deadline__lt=timezone.now()).count()

    return Response({
        'total': total,
        'by_status': {item['status']: item['count'] for item in by_status},
        'overdue': overdue,
    })


# Список и создание подзадач
class SubTaskListCreateView(ListCreateAPIView):
    queryset = SubTask.objects.select_related('task').all()
    serializer_class = SubTaskSerializer
    pagination_class = SubTaskPagination

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ('-created_at',)


# Получение по праймари ки, обновление и удаление подзадачи
class SubTaskDetailView(RetrieveUpdateDestroyAPIView):
   queryset = SubTask.objects.select_related('task').all()
   serializer_class = SubTaskSerializer

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=False, methods=['get'])
    def count_tasks(self, request):
        data = Category.objects.annotate(task_count=Count('task')).values('id', 'name', 'task_count')
        return Response(data)