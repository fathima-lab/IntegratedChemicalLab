from django.urls import path
from . import views


urlpatterns = [

    # View chemicals
    path(
        '',
        views.chemical_list,
        name='chemicals'
    ),

    # Register chemical
    path(
        'create/',
        views.create_chemical,
        name='create_chemical'
    ),

    # Edit chemical
    path(
        'edit/<int:chemical_id>/',
        views.edit_chemical,
        name='edit_chemical'
    ),

    # Remove chemical
    path(
        'delete/<int:chemical_id>/',
        views.delete_chemical,
        name='delete_chemical'
    ),

]