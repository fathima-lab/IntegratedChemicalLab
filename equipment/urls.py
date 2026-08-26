from django.urls import path
from . import views


urlpatterns = [

    # Equipment list
    path(
        '',
        views.equipment_list,
        name='equipment'
    ),

    # Create equipment
    path(
        'create/',
        views.create_equipment,
        name='create_equipment'
    ),

    # Update equipment
    path(
        'update/<int:equipment_id>/',
        views.update_equipment,
        name='update_equipment'
    ),

    # Remove equipment
    path(
        'remove/<int:equipment_id>/',
        views.remove_equipment,
        name='remove_equipment'
    ),
    path(
        'maintenance/',
        views.maintenance,
        name='maintenance'
    ),

    path(
        'maintenance/schedule/<int:equipment_id>/',
        views.schedule_maintenance,
        name='schedule_maintenance'
   ),

]