from django.conf import settings
from django.db import models


# ==========================================================
# LAB PROFILE
# ==========================================================

class LabProfile(models.Model):

    ROLE_CHOICES = [
        ('SUB_ADMIN', 'Sub Administrator'),
        ('RESEARCHER', 'Researcher'),
        ('TECHNICIAN', 'Technician'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='lab_profile'
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    supervisor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='supervised_lab_members'
    )

    department = models.CharField(
        max_length=150,
        blank=True
    )

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"


# ==========================================================
# LAB ACTIVITY
# ==========================================================

class LabActivity(models.Model):

    ACTIVITY_TYPES = [
        ('EXPERIMENT', 'Experiment'),
        ('SAMPLE', 'Sample'),
        ('CHEMICAL', 'Chemical'),
        ('EQUIPMENT', 'Equipment'),
        ('MAINTENANCE', 'Maintenance'),
        ('REPORT', 'Report'),
        ('OTHER', 'Other'),
    ]

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='lab_activities'
    )

    activity_type = models.CharField(
        max_length=30,
        choices=ACTIVITY_TYPES
    )

    description = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.actor.username} - {self.activity_type}"