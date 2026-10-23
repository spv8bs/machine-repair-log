from django.core.validators import MinValueValidator
from django.db import models

class Technician(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    position = models.CharField(max_length=30)
    email = models.EmailField(blank=True)

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True)

class Part(models.Model):
    name = models.CharField(max_length=100)
    catalog_number = models.CharField(unique=True)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2,
                                     validators=[MinValueValidator(0)])
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name="parts")


def __str__(self):
    return self.model