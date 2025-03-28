"""
URL configuration for CProgram project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Question import views 
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from usermode import views as usermode_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('usermode/', include('usermode.urls', namespace='usermode')),
    path('questions/', include('Question.urls', namespace='Question')),  
    # path('', lambda request: redirect('usermode:login'), name='home'),
    path('', usermode_views.login_view, name='home'),
]
