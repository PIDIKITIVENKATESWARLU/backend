from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Task
from .serializers import TaskSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# User Authentication Views

from django.contrib.auth.models import User  # Import User model

@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        data = request.data
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if User.objects.filter(username=username).exists():  # Correct reference to User model
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=password)  # Correct reference to User model
        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login_user(request):
    if request.method == 'POST':
        data = request.data
        username = data.get('username')
        password = data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def logout_user(request):
    logout(request)
    return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)


# Task Management Views

@api_view(['POST'])
def create_task(request):
    if request.method == 'POST':
        data = request.data
        user = request.user  # Assuming the user is logged in
        
        title = data.get('title')
        description = data.get('description')
        priority = data.get('priority')
        status = data.get('status')
        deadline = data.get('deadline')

        task = Task.objects.create(
            user=user, title=title, description=description,
            priority=priority, status=status, deadline=deadline
        )
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_task_list(request):
    tasks = Task.objects.filter(user=request.user)
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    serializer = TaskSerializer(task)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    data = request.data

    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.priority = data.get('priority', task.priority)
    task.status = data.get('status', task.status)
    task.deadline = data.get('deadline', task.deadline)
    
    task.save()
    serializer = TaskSerializer(task)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return Response({"message": "Task deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
from django.http import JsonResponse

def create_task(request):
    try:
        # Task creation logic
        return JsonResponse({"success": True}, status=201)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    

