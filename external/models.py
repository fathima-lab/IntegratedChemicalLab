from django.conf import settings
from django.db import models


class ExternalOrder(models.Model):

    ORDER_TYPE_CHOICES = [
        ('CHEMICAL', 'Chemical Purchase'),
        ('EQUIPMENT', 'Equipment Booking'),
        ('REPORT', 'Report Access'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending Payment'),
        ('PAID', 'Paid'),
        ('CANCELLED', 'Cancelled'),
        ('COMPLETED', 'Completed'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='external_orders'
    )

    order_type = models.CharField(
        max_length=20,
        choices=ORDER_TYPE_CHOICES
    )

    description = models.CharField(
        max_length=255
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return (
            f"{self.user.username} - "
            f"{self.get_order_type_display()}"
        )


class EquipmentBooking(models.Model):

    STATUS_CHOICES = [
        ('PENDING', 'Pending Payment'),
        ('CONFIRMED', 'Confirmed'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='external_equipment_bookings'
    )

    equipment = models.ForeignKey(
        'equipment.Equipment',
        on_delete=models.CASCADE,
        related_name='external_bookings'
    )

    booking_date = models.DateField()

    start_time = models.TimeField()

    end_time = models.TimeField()

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.user.username} - "
            f"{self.equipment.name} - "
            f"{self.booking_date}"
        )
