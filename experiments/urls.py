from django.urls import path
from . import views


urlpatterns = [

    path(
        '',
        views.experiments,
        name='experiments'
    ),

    path(
        'create/',
        views.create_experiment,
        name='create_experiment'
    ),

    path(
        'view/<int:experiment_id>/',
        views.view_experiment,
        name='view_experiment'
    ),

    path(
        'edit/<int:experiment_id>/',
        views.edit_experiment,
        name='edit_experiment'
    ),

    path(
        'delete/<int:experiment_id>/',
        views.delete_experiment,
        name='delete_experiment'
    ),

]