from django.db import models
from django.conf import settings


class Sample(models.Model):

    STATUS_CHOICES = [
        ('RECEIVED', 'Received'),
        ('PROCESSING', 'Processing'),
        ('ANALYZED', 'Analyzed'),
        ('STORED', 'Stored'),
        ('DISPOSED', 'Disposed'),
    ]

    researcher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='samples'
    )

    name = models.CharField(
        max_length=200
    )

    sample_code = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.TextField(
        blank=True
    )
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
   )

    unit = models.CharField(
        max_length=50,
        blank=True
    )

    storage_condition = models.CharField(
        max_length=255,
        blank=True
    )

    collection_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='RECEIVED'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.name} ({self.sample_code})"
