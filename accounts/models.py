from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    phone = models.CharField(
        max_length=15,
        blank=True
    )

    role = models.CharField(
        max_length=30,
        default='RESEARCHER'
    )

    external_type = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.username