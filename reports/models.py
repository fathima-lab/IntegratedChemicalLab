from django.db import models
from django.conf import settings


class Report(models.Model):

    # Researcher who created the report
    researcher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='lab_reports'
    )

    # Experiment associated with the report
    experiment = models.ForeignKey(
        'experiments.Experiment',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reports'
    )

    # Report title
    title = models.CharField(
        max_length=200
    )

    # Date of report
    report_date = models.DateField(
        null=True,
        blank=True
    )

    # What was observed during the experiment
    observations = models.TextField(
        blank=True
    )

    # Results obtained from the experiment
    results = models.TextField(
        blank=True
    )

    # Final interpretation/conclusion
    conclusion = models.TextField(
        blank=True
    )

    # Automatically recorded
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title