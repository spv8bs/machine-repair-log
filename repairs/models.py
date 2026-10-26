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
    limited_on = models.DateTimeField(null=True, blank=True)  # Machine operating with limitations
    diagnosis = models.TextField(blank=True)
    cost = models.DecimalField(max_digits=8, decimal_places=2, default=0,
                               validators=[MinValueValidator(0)])
    # status = models.BooleanField(default=False)
    photo = models.ImageField(upload_to="repairs/", blank=True)
    technicians = models.ManyToManyField(Technician, blank=True, related_name="repairs")
    parts = models.ManyToManyField(Part, blank=True, related_name="repairs")

    @property
    def is_resolved(self):
        return self.resolved_on is not None

    @property
    def downtime_end(self):
        ends = [d for d in (self.limited_on, self.resolved_on) if d]
        return min(ends) if ends else None

    @property
    def status(self):
        if self.resolved_on:
            return "Resolved"
        if self.limited_on:
            return "Limited"
        return "Open"

    # auto-generated repair number -> R-2026-0007 (year+id)
    @property
    def number(self):
        return f"R-{self.detected_on:%Y}-{self.pk:04d}"

    def __str__(self):
        if self.component is None:
            return f"{self.machine}"
        return f"{self.machine} - {self.component.component_type}"

class RepairAction(models.Model):
    repair = models.ForeignKey(Repair, on_delete=models.CASCADE, related_name="actions")
    technician = models.ForeignKey(Technician, on_delete=models.SET_NULL,
                                   null=True, blank=True, related_name="actions")
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if not self.description:
            return f"{self.repair} - NOT SPECIFIED"
        return f"{self.repair} - {self.description}"