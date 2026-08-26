from django.db import models
from django.conf import settings


class Equipment(models.Model):

    STATUS_CHOICES = [
        ('AVAILABLE', 'Available'),
        ('IN_USE', 'In Use'),
        ('MAINTENANCE', 'Under Maintenance'),
        ('OUT_OF_SERVICE', 'Out of Service'),
    ]

    # Researcher who registered the equipment
    researcher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='equipment_records'
    )

    name = models.CharField(
        max_length=200
    )

    equipment_id = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    manufacturer = models.CharField(
        max_length=200,
        blank=True
    )

    model_number = models.CharField(
        max_length=100,
        blank=True
    )

    location = models.CharField(
        max_length=200,
        blank=True
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='AVAILABLE'
    )

    purchase_date = models.DateField(
        null=True,
        blank=True
    )

    last_maintenance = models.DateField(
        null=True,
        blank=True
    )

    next_maintenance = models.DateField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.equipment_id})"
class Maintenance(models.Model):

    MAINTENANCE_TYPE_CHOICES = [
        ('PREVENTIVE', 'Preventive Maintenance'),
        ('CORRECTIVE', 'Corrective Maintenance'),
        ('EMERGENCY', 'Emergency Maintenance'),
    ]

    STATUS_CHOICES = [
        ('SCHEDULED', 'Scheduled'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    # Equipment being maintained
    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.CASCADE,
        related_name='maintenance_records'
    )

    # User who scheduled the maintenance
    scheduled_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='scheduled_maintenance'
    )

    maintenance_type = models.CharField(
        max_length=30,
        choices=MAINTENANCE_TYPE_CHOICES,
        default='PREVENTIVE'
    )

    scheduled_date = models.DateField()

    description = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='SCHEDULED'
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-scheduled_date']

    def __str__(self):
        return (
            f"{self.equipment.name} - "
            f"{self.scheduled_date}"
        )