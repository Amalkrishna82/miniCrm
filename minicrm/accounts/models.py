from django.db import models
from django.contrib.auth.models import User

ROLE_CHOICES = (
    ('Admin', 'Admin'),
    ('Manager', 'Manager'),
    ('Staff', 'Staff'),
)

STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('Approved', 'Approved'),
    ('Rejected', 'Rejected'),
)

class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.TextField()
    phone = models.BigIntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_company')
    industry = models.CharField(max_length=80,null=True, blank=True)

    def __str__(self):
        return self.name


class CompanyUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Approved')
    joined_at = models.DateTimeField(auto_now_add=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    class Meta:
        unique_together = ('user', 'company')

    def __str__(self):
        return self.user.username



