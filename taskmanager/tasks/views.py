from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Task
from rest_framework.permissions import AllowAny
from .permissions import IsOwner
from .serializers import UserSerializer, TaskSerializer
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status



# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    # only have to show the logged-in user's data can't see other users or their data
    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    def get_permissions(self):
        if self.action == 'create':  # signup(when creating new acc/register)
            return [AllowAny()]
        return super().get_permissions()

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsOwner]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['status', 'priority', 'due_date']
    search_fields = ['title', 'description']
    ordering_fields = ['due_date', 'priority']
    ordering = ['due_date']

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def mark_complete(self, request, pk=None):
        task = self.get_object()
        if task.status == 'Completed':
            return Response({'status': 'Task already Completed'}, status=status.HTTP_400_BAD_REQUEST)
        task.status = 'Completed'
        task.save()
        return Response({'status': 'Task marked completed', 'completed_at': task.completed_at}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def mark_pending(self, request, pk=None):
        task= self.get_object()
        if task.status == 'Pending':
            return Response({'status': 'Task already pending'}, status.HTTP_400_BAD_REQUEST)
        task.status = 'Pending'
        task.save()
        return Response({'status': 'Task reverted to Pending'}, status=status.HTTP_200_OK)