from django.urls import path
from . import views


urlpatterns = [

    path(
        '',
        views.reports,
        name='reports'
    ),

    path(
        'create/',
        views.create_report,
        name='create_report'
    ),

    path(
        'edit/<int:report_id>/',
        views.edit_report,
        name='edit_report'
    ),

    path(
        'delete/<int:report_id>/',
        views.delete_report,
        name='delete_report'
    ),

]