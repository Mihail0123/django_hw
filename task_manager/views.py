from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

from .models import Task, SubTask
from .pagionation import SubTaskPagination
from .serializers import TaskSerializer, SubTaskSerializer, SubTaskCreateSerializer


# Create your views here.

# Список задач + создание новой задачи
@api_view(['GET', 'POST'])
def task_list_create(request):
    if request.method == 'GET':
        day_param = request.query_params.get('day')

        if day_param:
            days_map = {
                'monday': 0,
                'tuesday': 1,
                'wednesday': 2,
                'thursday': 3,
                'friday': 4,
                'saturday': 5,
                'sunday': 6
            }
            day_param = day_param.lower()

            if day_param in days_map:
                weekday = days_map[day_param]
                tasks = Task.objects.all()
                tasks = [task for task in tasks if task.deadline.weekday() == weekday]
            else:
                return Response({'error': 'Invalid day name'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            tasks = Task.objects.all()

        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Получение конкретной задачи по id
@api_view(['GET'])
def task_detail(request, pk):
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = TaskSerializer(task)
    return Response(serializer.data)

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
class SubTaskListCreateView(APIView):
    def get(self, request):
        task_title = request.query_params.get('task')
        status_param = request.query_params.get('status')
        subtasks = SubTask.objects.select_related('task').all().order_by('-created_at')
        if task_title:
            subtasks =subtasks.filter(task__title__icontains=task_title)
        if status_param:
            subtasks = subtasks.filter(status__iexact=status_param)
        paginator = SubTaskPagination()
        page = paginator.paginate_queryset(subtasks, request)
        serializer = SubTaskSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = SubTaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Получение по праймари ки, обновление и удаление подзадачи
class SubTaskDetailUpdateDeleteView(APIView):
    def get_object(self, pk):
        return get_object_or_404(SubTask, pk=pk)

    def get(self, request, pk):
        subtask = self.get_object(pk)
        serializer = SubTaskSerializer(subtask)
        return Response(serializer.data)

    def put(self, request, pk):
        subtask = self.get_object(pk)
        serializer = SubTaskCreateSerializer(subtask, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        subtask = self.get_object(pk)
        subtask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
