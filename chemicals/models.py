from django.db import models
from django.conf import settings


class Chemical(models.Model):



    STATUS_CHOICES = [
        ('AVAILABLE', 'Available'),
        ('LOW_STOCK', 'Low Stock'),
        ('EXPIRED', 'Expired'),
        ('DISPOSED', 'Disposed'),
    ]

    researcher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='chemical_records'
    )

    name = models.CharField(
        max_length=200
    )

    chemical_id = models.CharField(
        max_length=100,
        unique=True
    )

    formula = models.CharField(
        max_length=200,
        blank=True
    )

    cas_number = models.CharField(
        max_length=100,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    quantity = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        default=0
    )

    unit = models.CharField(
        max_length=30,
        default='g'
    )

    storage_location = models.CharField(
        max_length=200,
        blank=True
    )

    hazard_information = models.TextField(
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

    expiry_date = models.DateField(
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
        return f"{self.name} ({self.chemical_id})"
