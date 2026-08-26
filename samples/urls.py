from django.urls import path
from . import views


urlpatterns = [

    path(
        '',
        views.samples,
        name='samples'
    ),

    path(
        'create/',
        views.create_sample,
        name='create_sample'
    ),

    path(
        'edit/<int:sample_id>/',
        views.edit_sample,
        name='edit_sample'
    ),

    path(
        'delete/<int:sample_id>/',
        views.delete_sample,
        name='delete_sample'
    ),

]