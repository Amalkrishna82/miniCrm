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
from transaction import views

app_name = 'transaction'

urlpatterns = [
    path('orders/', views.OrderList.as_view(), name='order_list'),
    path('orders_add/', views.OrderAdd.as_view(), name='order_add'),
    path('orders_edit/<int:i>/', views.OrderUpdate.as_view(), name='order_edit'),
    path('orders_delete/<int:i>/', views.OrderDelete.as_view(), name='order_delete'),
    path('orders/<int:i>/', views.OrderDetail.as_view(), name='order_detail'),  # <-- detail URL
    path('orders_pending/', views.PendingOrderList.as_view(), name='order_pending'),
    path('services/', views.ServiceList.as_view(), name='service_list'),
    path('services_add/', views.ServiceAdd.as_view(), name='service_add'),
    path('services_edit/<int:i>/', views.ServiceUpdate.as_view(), name='service_edit'),
    path('services_delete/<int:i>/', views.ServiceDelete.as_view(), name='service_delete'),
    path('services/<int:i>/', views.ServiceDetail.as_view(), name='service_detail'),  # <-- detail URL
    path('services-completed/', views.CompletedServiceList.as_view(), name='completed_service'),
]


