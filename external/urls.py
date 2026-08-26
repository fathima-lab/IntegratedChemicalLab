from django.urls import path

from . import views


urlpatterns = [

    # External dashboard
    path(
        '',
        views.external_dashboard,
        name='external_dashboard'
    ),

    # Registration
    path(
        'register/',
        views.external_register,
        name='external_register'
    ),

    # Chemicals
    path(
        'chemicals/',
        views.external_chemicals,
        name='external_chemicals'
    ),

    # Equipment
    path(
        'equipment/',
        views.external_equipment,
        name='external_equipment'
    ),

    # Equipment booking
    path(
        'equipment/book/',
        views.external_equipment_booking,
        name='external_equipment_booking'
    ),

    # Reports
    path(
        'reports/',
        views.external_reports,
        name='external_reports'
    ),

     path(
        'reports/laboratory/',
        views.external_laboratory_reports,
        name='external_laboratory_reports'
    ),

    path(
        'reports/bookings/',
        views.external_booking_reports,
        name='external_booking_reports'
    ),

]