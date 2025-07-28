from django.db import models

from apps.core.models import BaseLog, Company


class Product(BaseLog):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    product_code = models.CharField(max_length=16)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    stock = models.IntegerField(default=0)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
    
