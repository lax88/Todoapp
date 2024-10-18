from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .models import TodoItem
from users.models import User
from .serializers import TodoItemSerializer 
from users.serializers import UserSerializer
from .permissions import IsOwnerOrAdmin
from django.shortcuts import get_object_or_404

class TodoItemViewSet(viewsets.ModelViewSet):
    queryset= TodoItem.objects.all()
    serializer_class = TodoItemSerializer
    permission_classes = [IsOwnerOrAdmin]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return TodoItem.objects.all()
        return TodoItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        if self.request.user.is_superuser:
            user_id = self.request.data.get('user')
            user = get_object_or_404(User, pk=user_id)
            serializer.save(user=user)

        else: 
            serializer.save(user=self.request.user)

        
