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
    # CENTRAL ADMINISTRATOR
    # ======================================================

    path(
        'create-sub-admin/',
        views.create_sub_admin,
        name='create_sub_admin'
    ),

    path(
        'edit-sub-admin/<int:user_id>/',
        views.edit_sub_admin,
        name='edit_sub_admin'
    ),

    path(
        'delete-sub-admin/<int:user_id>/',
        views.delete_sub_admin,
        name='delete_sub_admin'
    ),


    # ======================================================
    # SUB-ADMINISTRATOR
    # ======================================================

    path(
        'create-team-member/',
        views.create_team_member,
        name='create_team_member'
    ),

    path(
        'edit-team-member/<int:user_id>/',
        views.edit_team_member,
        name='edit_team_member'
    ),

    path(
        'delete-team-member/<int:user_id>/',
        views.delete_team_member,
        name='delete_team_member'
    ),


    # ======================================================
    # RESEARCHER MODULES
    # ======================================================

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