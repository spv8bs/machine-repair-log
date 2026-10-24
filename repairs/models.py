from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from machines.models import Machine, Component
from resources.models import Technician, Part


class Repair(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.PROTECT, related_name="repairs")   # protected -> for repair history!
    component = models.ForeignKey(Component, on_delete=models.SET_NULL,
                                  blank=True, null=True, related_name="repairs")
    problem = models.TextField()
    detected_on = models.DateTimeField(default=timezone.now)
    resolved_on = models.DateTimeField(null=True, blank=True)
    diagnosis = models.TextField(blank=True)
    downtime_minutes = models.PositiveIntegerField(default=0)
    cost = models.DecimalField(max_digits=8, decimal_places=2, default=0,
                               validators=[MinValueValidator(0)])
    status = models.BooleanField(default=False)
    photo = models.ImageField(upload_to="repairs/", blank=True)
    technicians = models.ManyToManyField(Technician, blank=True, related_name="repairs")
    parts = models.ManyToManyField(Part, blank=True, related_name="repairs")

    def __str__(self):
        return f"{self.machine} - {self.component}"

class RepairAction(models.Model):
    repair = models.ForeignKey(Repair, on_delete=models.CASCADE, related_name="actions")
    technician = models.ForeignKey(Technician, on_delete=models.SET_NULL,
                                   null=True, blank=True, related_name="actions")
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.repair} - {self.description}"