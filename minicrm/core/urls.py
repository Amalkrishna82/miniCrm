"""
URL configuration for minicrm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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

from django.urls import path
from core import views

app_name = 'core'

urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('leaves/', views.LeaveList.as_view(), name='leave_list'),
    path('leavesnew/', views.LeaveCreate.as_view(), name='leave_create'),
    path('leaves/<int:pk>/<str:action>/', views.LeaveAction.as_view(), name='leave_action'),
    path('search/', views.GlobalSearchView.as_view(), name='global_search'),
]

