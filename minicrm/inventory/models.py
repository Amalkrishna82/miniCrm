from django.db import models
from django.contrib.auth.models import User
from accounts.models import Company

SOURCE_CHOICES = (
    ('Bought', 'Bought'),
    ('Manufactured', 'Manufactured'),
)

class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    image = models.ImageField(upload_to='category/', default='default_category.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES)
    buying_price = models.FloatField(null=True, blank=True)
    manufacture_price = models.FloatField(null=True, blank=True)
    selling_price = models.FloatField()
    min_selling_price = models.FloatField(default=0)
    sku = models.CharField(max_length=100, blank=True, help_text="Stock Keeping Unit (unique identifier)")
    specifications = models.TextField(blank=True)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='product/', default='default_product.jpg')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    @property
    def out_of_stock(self):
        return self.stock <= 0

    def __str__(self):
        return self.name
