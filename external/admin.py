from django.contrib import admin

from .models import (
    ExternalOrder,
    EquipmentBooking,
)


@admin.register(ExternalOrder)
class ExternalOrderAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'order_type',
        'amount',
        'status',
        'created_at',
    )

    list_filter = (
        'order_type',
        'status',
    )

    search_fields = (
        'user__username',
        'description',
    )


@admin.register(EquipmentBooking)
class EquipmentBookingAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'equipment',
        'booking_date',
        'start_time',
        'end_time',
        'amount',
        'status',
    )

    list_filter = (
        'status',
        'booking_date',
    )

    search_fields = (
        'user__username',
        'equipment__name',
        'equipment__equipment_id',
    )