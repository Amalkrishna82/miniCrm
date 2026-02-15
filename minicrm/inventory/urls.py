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
from inventory import views

app_name = 'inventory'

urlpatterns = [

    path('categories', views.CategoryList.as_view(), name='category_list'),
    path('categories-add', views.CategoryCreate.as_view(), name='category_create'),
    path('categories-edit/<int:pk>', views.CategoryUpdate.as_view(), name='category_edit'),
    path('categories-delete/<int:pk>', views.CategoryDelete.as_view(), name='category_delete'),
    path('products/<int:pk>', views.ProductList.as_view(), name='product_list'),
    path('products-details/<int:pk>', views.ProductDetail.as_view(), name='product_detail'),
    path('products-add/', views.ProductCreate.as_view(), name='product_add'),
    path('products-edit/<int:pk>', views.ProductUpdate.as_view(), name='product_edit'),
    path('products-delete/<int:pk>', views.ProductDelete.as_view(), name='product_delete'),
    path('products-stock/<int:pk>', views.StockUpdate.as_view(), name='stock_update'),
    path('<int:pk>/stock/increase/', views.IncreaseStock.as_view(), name='stock_increase'),
    path('<int:pk>/stock/decrease/', views.DecreaseStock.as_view(), name='stock_decrease'),
    path('all-products', views.AllproductsList.as_view(), name='all_products'),
]

