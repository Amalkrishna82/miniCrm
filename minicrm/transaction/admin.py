from django.contrib import admin

from transaction.models import Service,OrderItem,Order



admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Service)
