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
from accounts import views

app_name = 'accounts'
urlpatterns = [

    path('signup/', views.SignupView.as_view(), name='register'),
    path('', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('selection/', views.SelectionView.as_view(), name='selection'),
    path('start-company/', views.StartCompanyView.as_view(), name='start_company'),
    path('join-company/', views.JoinCompanyView.as_view(), name='join_company'),
    path('pending-users/', views.PendingUserListView.as_view(), name='pending_user_list'),


    path('adminadd-user/', views.AdminAddUserView.as_view(), name='adminadduser'),
    path('adminapprove/<int:pk>/', views.ApproveUserView.as_view(), name='approve_user'),
    path('companyusers/', views.CompanyUserListView.as_view(), name='user_list'),
    path('companyuser/<int:pk>/', views.UserManageView.as_view(), name='user_manage'),

    path('select-company/', views.SelectCompanyView.as_view(), name='select_company'),
]


