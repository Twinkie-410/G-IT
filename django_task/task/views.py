from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView

from task.models import Task
from task.serializer import TaskSerializer


class TaskCreateAPIView(CreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = []


class TaskListAPIView(ListAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = []


class TaskDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = []
    lookup_field = "id"
