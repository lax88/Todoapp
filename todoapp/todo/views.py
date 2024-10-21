from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .models import TodoItem
from users.models import User
from .serializers import TodoItemSerializer 
from users.serializers import UserSerializer
from todo.utils.permissions import IsOwnerOrAdmin
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages


class TodoItemViewSet(viewsets.ModelViewSet):
    queryset= TodoItem.objects.all()
    serializer_class = TodoItemSerializer
    permission_classes = [IsOwnerOrAdmin]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_superuser:
                return TodoItem.objects.all()
            return TodoItem.objects.filter(user=self.request.user)
        else:
            return TodoItem.objects.none()

    def perform_create(self, serializer):
        if self.request.user.is_superuser:
            user_id = self.request.data.get('user')
            user = get_object_or_404(User, pk=user_id)
            serializer.save(user=user)

        else: 
            serializer.save(user=self.request.user)
            
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('todo-list')  # Redirect to todo list after successful login
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'users/login.html') 

@login_required
def todo_list_view(request):
        todos= TodoItem.objects.filter(user=request.user) if request.user.is_authenticated else[]
        return render(request, 'todo/todo_list.html',{'todos':todos})

@login_required
def add_todo_view(request):
        if request.method == "POST":
            title = request.POST.get('title')
            if title:
                TodoItem.objects.create(title=title, user=request.user)
                return redirect('todo-list')
        return render(request, 'todo/add_todo.html')
