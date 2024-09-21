from django.urls import path

from task.views import TaskCreateAPIView, TaskListAPIView, TaskDetailAPIView

urlpatterns = [
    path('create/', TaskCreateAPIView.as_view(), name='task-create'),
    path('get/', TaskListAPIView.as_view(), name='task-list'),
    path('<int:id>', TaskDetailAPIView.as_view(), name='task-detail'),
]
