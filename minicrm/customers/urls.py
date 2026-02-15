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
from . import views

app_name = 'customers'

urlpatterns = [

    path('leadadd/', views.LeadAdd.as_view(), name='lead_add'),
    path('leadlist/', views.LeadList.as_view(), name='lead_list'),
    path('leadupdate/<int:i>/', views.LeadUpdate.as_view(), name='lead_update'),
    path('leaddelete/<int:i>/', views.LeadDelete.as_view(), name='lead_delete'),
    path('customerlist/', views.CustomerList.as_view(), name='customer_list'),
    path('customeradd/', views.CustomerAdd.as_view(), name='customer_add'),
    path('customerupdate/<int:i>/', views.CustomerUpdate.as_view(), name='customer_update'),
    path('customerdelete/<int:i>/', views.CustomerDelete.as_view(), name='customer_delete'),
]


