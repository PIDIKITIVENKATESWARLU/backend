from rest_framework import serializers
from .models import Task
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class TaskSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Task
        fields = ['id', 'user', 'title', 'description', 'priority', 'status', 'deadline']
        class UserSerializer(serializers.ModelSerializer):
           class Meta:
              model = User
    fields = ['id', 'username', 'email']

