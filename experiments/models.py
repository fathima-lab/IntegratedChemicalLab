from django.db import models
from django.conf import settings


class Experiment(models.Model):

    STATUS_CHOICES = [
        ('PLANNED', 'Planned'),
        ('ONGOING', 'Ongoing'),
        ('COMPLETED', 'Completed'),
    ]

    researcher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='experiments'
    )

    name = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True
    )

    results_observations = models.TextField(
        blank=True,
        verbose_name="Results & Observations"
    )

    conclusion = models.TextField(
        blank=True,
        verbose_name="Conclusion"
    )

    start_date = models.DateField(
        null=True,
        blank=True
    )

    end_date = models.DateField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PLANNED'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name