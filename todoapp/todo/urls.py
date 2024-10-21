from django.urls import path, include
from .views import TodoItemViewSet, todo_list_view, add_todo_view
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'/todos', TodoItemViewSet, basename='todo')

urlpatterns = [
    path('todos/', todo_list_view, name='todo-list'),  # List of todos
    path('todos/add/', add_todo_view, name='add-todo'),  # Add new todo
    path('api/', include(router.urls)),
]
