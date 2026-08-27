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

    path(
        'chemicals/purchase/<int:chemical_id>/',
        views.chemical_purchase,
        name='chemical_purchase'
    ),

    # Equipment
    path(
        'equipment/',
        views.external_equipment,
        name='external_equipment'
    ),

    # Equipment booking
    path(
        'equipment/book/<int:equipment_id>/',
        views.external_equipment_booking,
        name='external_equipment_booking'
    ),

    path(
        'reports/bookings/',
        views.external_booking_reports,
        name='external_booking_reports'
    ),

]