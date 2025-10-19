from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Task
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import IsOwner
from .serializers import UserSerializer, TaskSerializer
from rest_framework import viewsets, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response


# -------------------------------
# USER VIEWSET
# -------------------------------
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Admins can see all users
        if user.is_staff or user.is_superuser:
            return User.objects.all()
        # Normal users can only see themselves
        return User.objects.filter(id=user.id)

    def get_permissions(self):
        if self.action == 'create':  # allow registration
            return [AllowAny()]
        return super().get_permissions()

    # --- Custom success messages ---
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = {
            "detail": "User created successfully",
            "user": response.data
        }
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response.data = {
            "detail": "User updated successfully",
            "user": response.data
        }
        return response

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        username = instance.username
        self.perform_destroy(instance)
        return Response(
            {"detail": f"User '{username}' deleted successfully"},
            status=status.HTTP_200_OK
        )


# -------------------------------
# TASK VIEWSET
# -------------------------------
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

    # --- Custom success messages ---
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = {
            "detail": "Task created successfully",
            "task": response.data
        }
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response.data = {
            "detail": "Task updated successfully",
            "task": response.data
        }
        return response

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        title = instance.title
        self.perform_destroy(instance)
        return Response(
            {"detail": f"Task '{title}' deleted successfully"},
            status=status.HTTP_200_OK
        )

    # --- Custom actions for mark complete/uncomplete ---
    @action(detail=True, methods=['post'])
    def mark_complete(self, request, pk=None):
        task = self.get_object()
        if task.status == 'Completed':
            return Response(
                {"detail": "Task is already completed"},
                status=status.HTTP_400_BAD_REQUEST
            )
        task.status = 'Completed'
        task.save()
        return Response(
            {"detail": "Task marked as completed", "task_id": task.id},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'])
    def mark_pending(self, request, pk=None):
        task = self.get_object()
        if task.status == 'Pending':
            return Response(
                {"detail": "Task is already pending"},
                status=status.HTTP_400_BAD_REQUEST
            )
        task.status = 'Pending'
        task.save()
        return Response(
            {"detail": "Task reverted to pending", "task_id": task.id},
            status=status.HTTP_200_OK
        )
