from django.db import models
from users.models import User
from django.conf import settings

class TodoItem(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE, related_name='todo_items')

    def __str__(self):
        return self.title
    
    