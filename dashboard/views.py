from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import LabProfile, LabActivity
from .forms import SubAdminForm, TeamMemberForm

# ==========================================================
# HOME
# ==========================================================

def home(request):
    return render(request, 'home.html')


# ==========================================================
# ABOUT
# ==========================================================

def about(request):
    return render(request, 'about.html')


# ==========================================================
# FEATURES
# ==========================================================

def features(request):
    return render(request, 'features.html')


# ==========================================================
# CONTACT
# ==========================================================

def contact(request):
    return render(request, 'contact.html')


# ==========================================================
# CENTRAL ADMINISTRATOR DASHBOARD
# ==========================================================

@login_required
def dashboard(request):

    # Central Administrator only
    if not request.user.is_superuser:

        return render(
            request,
            'dashboard.html',
            {
                'access_denied': True
            }
        )

    # ------------------------------------------------------
    # ALL SUB-ADMINISTRATORS
    # ------------------------------------------------------

    sub_admin_profiles = (
        LabProfile.objects
        .filter(role='SUB_ADMIN')
        .select_related('user')
    )

    # ------------------------------------------------------
    # COUNTS
    # ------------------------------------------------------

    total_sub_admins = sub_admin_profiles.count()

    total_researchers = (
        LabProfile.objects
        .filter(role='RESEARCHER')
        .count()
    )

    total_technicians = (
        LabProfile.objects
        .filter(role='TECHNICIAN')
        .count()
    )

    total_activities = LabActivity.objects.count()

    # ------------------------------------------------------
    # BUILD BRANCH INFORMATION
    # ------------------------------------------------------

    sub_admin_data = []

    for sub_admin_profile in sub_admin_profiles:

        sub_admin = sub_admin_profile.user

        # Researchers under this Sub-Administrator
        researchers = (
            LabProfile.objects
            .filter(
                role='RESEARCHER',
                supervisor=sub_admin
            )
            .select_related('user')
        )

        # Technicians under this Sub-Administrator
        technicians = (
            LabProfile.objects
            .filter(
                role='TECHNICIAN',
                supervisor=sub_admin
            )
            .select_related('user')
        )

        # User IDs for activity monitoring
        researcher_ids = list(
            researchers.values_list(
                'user_id',
                flat=True
            )
        )

        technician_ids = list(
            technicians.values_list(
                'user_id',
                flat=True
            )
        )

        member_ids = researcher_ids + technician_ids

        # Activities of researchers and technicians
        activities = (
            LabActivity.objects
            .filter(
                actor_id__in=member_ids
            )
            .select_related('actor')
            .order_by('-created_at')[:10]
        )

        sub_admin_data.append({
            'profile': sub_admin_profile,
            'user': sub_admin,
            'researchers': researchers,
            'technicians': technicians,
            'activities': activities,
        })

    # ------------------------------------------------------
    # ALL RECENT LABORATORY ACTIVITIES
    # ------------------------------------------------------

    recent_activities = (
        LabActivity.objects
        .select_related('actor')
        .order_by('-created_at')[:15]
    )

    # ------------------------------------------------------
    # CONTEXT
    # ------------------------------------------------------

    context = {
        'sub_admin_data': sub_admin_data,
        'total_sub_admins': total_sub_admins,
        'total_researchers': total_researchers,
        'total_technicians': total_technicians,
        'total_activities': total_activities,
        'recent_activities': recent_activities,
    }

    return render(
        request,
        'dashboard.html',
        context
    )


# ==========================================================
# SUB-ADMINISTRATOR DASHBOARD
# ==========================================================

@login_required
def sub_admin_dashboard(request):

    # Get current user's Sub-Administrator profile
    try:

        profile = LabProfile.objects.get(
            user=request.user,
            role='SUB_ADMIN'
        )

    except LabProfile.DoesNotExist:

        return render(
            request,
            'sub_admin_dashboard.html',
            {
                'access_denied': True
            }
        )

    # ------------------------------------------------------
    # RESEARCHERS
    # ------------------------------------------------------

    researchers = (
        LabProfile.objects
        .filter(
            role='RESEARCHER',
            supervisor=request.user
        )
        .select_related('user')
    )

    # ------------------------------------------------------
    # TECHNICIANS
    # ------------------------------------------------------

    technicians = (
        LabProfile.objects
        .filter(
            role='TECHNICIAN',
            supervisor=request.user
        )
        .select_related('user')
    )

    # ------------------------------------------------------
    # TEAM USER IDS
    # ------------------------------------------------------

    researcher_ids = list(
        researchers.values_list(
            'user_id',
            flat=True
        )
    )

    technician_ids = list(
        technicians.values_list(
            'user_id',
            flat=True
        )
    )

    member_ids = researcher_ids + technician_ids

    # ------------------------------------------------------
    # TEAM ACTIVITIES
    # ------------------------------------------------------

    activities = (
        LabActivity.objects
        .filter(
            actor_id__in=member_ids
        )
        .select_related('actor')
        .order_by('-created_at')[:15]
    )

    context = {
        'profile': profile,
        'researchers': researchers,
        'technicians': technicians,
        'activities': activities,
        'total_researchers': researchers.count(),
        'total_technicians': technicians.count(),
    }

    return render(
        request,
        'sub_admin_dashboard.html',
        context
    )


# ==========================================================
# RESEARCHER DASHBOARD
# ==========================================================

@login_required
def researcher_dashboard(request):

    activities = (
        LabActivity.objects
        .filter(actor=request.user)
        .select_related('actor')
        .order_by('-created_at')[:15]
    )

    return render(
        request,
        'researcher_dashboard.html',
        {
            'activities': activities
        }
    )


# ==========================================================
# TECHNICIAN DASHBOARD
# ==========================================================

@login_required
def technician_dashboard(request):

    activities = (
        LabActivity.objects
        .filter(actor=request.user)
        .select_related('actor')
        .order_by('-created_at')[:15]
    )

    return render(
        request,
        'technician_dashboard.html',
        {
            'activities': activities
        }
    )


# ==========================================================
# CREATE SUB-ADMINISTRATOR
# ==========================================================

@login_required
def create_sub_admin(request):

    # Central Administrator only
    if not request.user.is_superuser:

        return render(
            request,
            'create_sub_admin.html',
            {
                'access_denied': True
            }
        )

    # ------------------------------------------------------
    # POST
    # ------------------------------------------------------

    if request.method == 'POST':

        form = SubAdminForm(request.POST)

        if form.is_valid():

            # Create user
            user = form.save()

            # Create Sub-Administrator profile
            LabProfile.objects.update_or_create(
                user=user,
                defaults={
                    'role': 'SUB_ADMIN',
                    'supervisor': None,
                }
            )

            # --------------------------------------------------
            # RECORD ACTIVITY
            # --------------------------------------------------
            # LabActivity has:
            # actor
            # activity_type
            # description
            #
            # It does NOT have an "action" field.

            LabActivity.objects.create(
                actor=request.user,
                activity_type='OTHER',
                description=(
                    f'Created Sub-Administrator: '
                    f'{user.username}'
                )
            )

            messages.success(
                request,
                f'Sub-Administrator "{user.username}" '
                f'created successfully.'
            )

            return redirect('dashboard')

    else:

        form = SubAdminForm()

    # ------------------------------------------------------
    # DISPLAY FORM
    # ------------------------------------------------------

    return render(
        request,
        'create_sub_admin.html',
        {
            'form': form
        }
    )

# ==========================================================
# CREATE RESEARCHER / TECHNICIAN
# ==========================================================

@login_required
def create_team_member(request):

    # ------------------------------------------------------
    # SUB-ADMINISTRATOR ONLY
    # ------------------------------------------------------

    try:

        profile = LabProfile.objects.get(
            user=request.user,
            role='SUB_ADMIN'
        )

    except LabProfile.DoesNotExist:

        return render(
            request,
            'create_team_member.html',
            {
                'access_denied': True
            }
        )

    # ------------------------------------------------------
    # FORM SUBMISSION
    # ------------------------------------------------------

    if request.method == 'POST':

        form = TeamMemberForm(request.POST)

        if form.is_valid():

            # Create User
            user = form.save()

            role = form.cleaned_data['role']

            # --------------------------------------------------
            # CREATE LAB PROFILE
            # --------------------------------------------------

            LabProfile.objects.create(

                user=user,

                role=role,

                # THIS ASSIGNS THE MEMBER TO THE
                # CURRENT SUB-ADMINISTRATOR
                supervisor=request.user,

            )

            # --------------------------------------------------
            # RECORD ACTIVITY
            # --------------------------------------------------

            LabActivity.objects.create(

                actor=request.user,

                activity_type='OTHER',

                description=(
                    f'Created '
                    f'{"Researcher" if role == "RESEARCHER" else "Technician"} '
                    f'{user.username}'
                )

            )

            messages.success(
                request,
                f'{user.username} was created successfully.'
            )

            return redirect(
                'sub_admin_dashboard'
            )

    else:

        form = TeamMemberForm()

    return render(
        request,
        'create_team_member.html',
        {
            'form': form,
            'profile': profile,
        }
    )

# ==========================================================
# RESEARCHER - EXPERIMENTS
# ==========================================================

@login_required
def experiments(request):

    return render(
        request,
        'experiments.html'
    )


# ==========================================================
# RESEARCHER - SAMPLES
# ==========================================================

@login_required
def samples(request):

    return render(
        request,
        'samples.html'
    )


# ==========================================================
# RESEARCHER - RESEARCH REPORTS
# ==========================================================

@login_required
def reports(request):

    return render(
        request,
        'reports.html'
    )

@login_required
def equipment(request):
    return render(request, 'equipment.html')


@login_required
def maintenance(request):
    return render(request, 'maintenance.html')


@login_required
def chemicals(request):
    return render(request, 'chemicals.html')