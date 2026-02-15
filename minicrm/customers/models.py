from django.db import models
from django.contrib.auth.models import User
from accounts.models import Company

STATUS = [
    ('New', 'New'),
    ('Contacted', 'Contacted'),
    ('Converted', 'Converted'),
    ('NotConverted', 'NotConverted'),
]

class Customer(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Lead(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=32, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS, default='New')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='leads_created')
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    address = models.TextField()

    def __str__(self):
        return self.name

