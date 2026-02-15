from django.db import models
from django.contrib.auth.models import User
from accounts.models import Company
from inventory.models import Product
from customers.models import Customer,Lead

ORDER_STATUS = (
    ('Pending', 'Pending'),
    ('Completed', 'Completed'),)


class Order(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    total_amount = models.FloatField(default=0)
    total_profit = models.FloatField(default=0)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer.name


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    selling_price = models.FloatField(default=0)
    profit = models.FloatField(default=0)

    def __str__(self):
        return self.product.name


class Service(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    lead = models.ForeignKey(Lead, on_delete=models.SET_NULL, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()
    issue_description = models.TextField(blank=True, null=True)
    service_type = models.CharField(max_length=50)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    service_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='service_created_by')
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default="Pending")

    def __str__(self):
        return self.customer.name if self.customer else self.lead.name
