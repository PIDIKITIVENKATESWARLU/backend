from django.contrib import admin
from django.urls import path, include
# task_management/urls.py
from django.urls import path
from . import view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('task_manager.urls')),
]

