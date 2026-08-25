from django.urls import path
from . import views


urlpatterns = [

    # ======================================================
    # GENERAL PAGES
    # ======================================================

    path(
        '',
        views.home,
        name='home'
    ),

    path(
        'about/',
        views.about,
        name='about'
    ),

    path(
        'features/',
        views.features,
        name='features'
    ),

    path(
        'contact/',
        views.contact,
        name='contact'
    ),


    # ======================================================
    # DASHBOARDS
    # ======================================================

    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),

    path(
        'sub-admin/',
        views.sub_admin_dashboard,
        name='sub_admin_dashboard'
    ),

    path(
        'researcher/',
        views.researcher_dashboard,
        name='researcher_dashboard'
    ),

    path(
        'technician/',
        views.technician_dashboard,
        name='technician_dashboard'
    ),


    # ======================================================
    # RESEARCHER MODULES
    # ======================================================

    path(
        'experiments/',
        views.experiments,
        name='experiments'
    ),

    path(
        'samples/',
        views.samples,
        name='samples'
    ),

    path(
        'reports/',
        views.reports,
        name='reports'
    ),

    path(
        'equipment/',
        views.equipment,
        name='equipment'
    ),

    path(
        'maintenance/',
        views.maintenance,
        name='maintenance'
    ),

    path(
        'chemicals/',
        views.chemicals,
        name='chemicals'
    ),

]