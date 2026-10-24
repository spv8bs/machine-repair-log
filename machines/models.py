from django.core.validators import MinLengthValidator
from django.db import models

class Machine(models.Model):
    model = models.CharField(max_length=50,
                             unique=True,
                             validators=[MinLengthValidator(3)]) # machine brand + model
    machine_type = models.CharField(max_length=50) # laminator, printer, etc.
    location = models.CharField(max_length=30, blank=True) # lamination, print house, etc.
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.model

class Component(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name="components")
    component_type = models.CharField(max_length=50) # main motor, print section bearing, etc.
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.machine.model} - {self.component_type}"