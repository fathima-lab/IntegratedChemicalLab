from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import LabProfile, LabActivity
from .forms import SubAdminForm, TeamMemberForm

from experiments.models import Experiment
from chemicals.models import Chemical
from equipment.models import Equipment


# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def get_user_institution(user):
    """
    Safely get the institution/company belonging to a user.
    """
    return getattr(user, 'institution', '') or ''


def get_activity_text(activity):
    """
    Return activity text without repeating the username.

    Example database description:
        'shyam_technician - CHEMICAL'

    Display:
        'Chemical'

    If the description contains useful information such as:
        'Added Chemical: Hydrochloric Acid'

    it is preserved.
    """

    description = getattr(activity, 'description', '') or ''
    username = ''

    if getattr(activity, 'actor', None):
        username = getattr(activity.actor, 'username', '') or ''

    # ------------------------------------------------------
    # Remove username prefix
    # ------------------------------------------------------
    if username:
        prefixes = [
            f'{username} - ',
            f'{username}-',
            f'{username} – ',
            f'{username} — ',
            f'{username}: ',
        ]

        for prefix in prefixes:
            if description.startswith(prefix):
                description = description[len(prefix):].strip()
                break

    # ------------------------------------------------------
    # Remove username if it appears as the first word
    # ------------------------------------------------------
    if username and description.startswith(username):
        description = description[len(username):].strip(
            ' -–—:'
        )

    # ------------------------------------------------------
    # If description is empty, use activity type
    # ------------------------------------------------------
    if not description:
        activity_type = getattr(
            activity,
            'activity_type',
            ''
        ) or ''

        mapping = {
            'CHEMICAL': 'Chemical activity',
            'EQUIPMENT': 'Equipment activity',
            'MAINTENANCE': 'Maintenance activity',
            'EXPERIMENT': 'Experiment completed',
            'SAMPLE': 'Sample activity',
            'REPORT': 'Report activity',
            'OTHER': 'Other activity',
        }

        description = mapping.get(
            activity_type,
            activity_type.replace('_', ' ').title()
            if activity_type
            else 'Laboratory activity'
        )

    return description


def prepare_activities(activities):
    """
    Add a template-friendly activity_display attribute.

    The original database description is not changed.
    """

    for activity in activities:
        activity.activity_display = get_activity_text(
            activity
        )

    return activities


def get_sub_admin_profile(user):
    """
    Get the current user's Sub-Administrator profile.

    Important:
    If CustomUser.role is SUB_ADMIN but the LabProfile is
    missing, create it automatically.

    This fixes the permission-denied problem that occurs
    when the user exists as a Sub-Administrator but has no
    LabProfile row.
    """

    # ------------------------------------------------------
    # First try LabProfile
    # ------------------------------------------------------
    try:
        return (
            LabProfile.objects
            .select_related('user')
            .get(
                user=user,
                role='SUB_ADMIN'
            )
        )

    except LabProfile.DoesNotExist:
        pass

    # ------------------------------------------------------
    # FALLBACK:
    # Check CustomUser.role
    # ------------------------------------------------------
    user_role = getattr(
        user,
        'role',
        ''
    )

    if user_role == 'SUB_ADMIN':

        profile, created = (
            LabProfile.objects
            .get_or_create(
                user=user,
                defaults={
                    'role': 'SUB_ADMIN',
                    'supervisor': None,
                }
            )
        )

        # If an existing profile has a wrong role,
        # correct it.
        if profile.role != 'SUB_ADMIN':
            profile.role = 'SUB_ADMIN'
            profile.supervisor = None
            profile.save(
                update_fields=[
                    'role',
                    'supervisor'
                ]
            )

        return profile

    return None


# ==========================================================
# HOME
# ==========================================================

def home(request):
    return render(
        request,
        'home.html'
    )


# ==========================================================
# ABOUT
# ==========================================================

def about(request):
    return render(
        request,
        'about.html'
    )


# ==========================================================
# FEATURES
# ==========================================================

def features(request):
    return render(
        request,
        'features.html'
    )


# ==========================================================
# CONTACT
# ==========================================================

def contact(request):
    return render(
        request,
        'contact.html'
    )


# ==========================================================
# CENTRAL ADMINISTRATOR DASHBOARD
# ==========================================================

@login_required
def dashboard(request):

    # ------------------------------------------------------
    # CENTRAL ADMINISTRATOR ONLY
    # ------------------------------------------------------

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
        .filter(
            role='SUB_ADMIN'
        )
        .select_related('user')
        .order_by(
            'user__first_name',
            'user__last_name'
        )
    )

    # ------------------------------------------------------
    # GLOBAL COUNTS
    # ------------------------------------------------------

    total_sub_admins = (
        sub_admin_profiles.count()
    )

    total_researchers = (
        LabProfile.objects
        .filter(
            role='RESEARCHER'
        )
        .count()
    )

    total_technicians = (
        LabProfile.objects
        .filter(
            role='TECHNICIAN'
        )
        .count()
    )

    total_activities = (
        LabActivity.objects.count()
    )

    # ------------------------------------------------------
    # BUILD EACH SUB-ADMINISTRATOR BRANCH
    # ------------------------------------------------------

    sub_admin_data = []

    for sub_admin_profile in sub_admin_profiles:

        sub_admin = (
            sub_admin_profile.user
        )

        # --------------------------------------------------
        # INSTITUTION / COMPANY
        # --------------------------------------------------

        institution_name = (
            get_user_institution(
                sub_admin
            )
        )

        # --------------------------------------------------
        # RESEARCHERS
        # --------------------------------------------------

        researchers = (
            LabProfile.objects
            .filter(
                role='RESEARCHER',
                supervisor=sub_admin
            )
            .select_related('user')
            .order_by(
                'user__first_name',
                'user__last_name'
            )
        )

        # --------------------------------------------------
        # TECHNICIANS
        # --------------------------------------------------

        technicians = (
            LabProfile.objects
            .filter(
                role='TECHNICIAN',
                supervisor=sub_admin
            )
            .select_related('user')
            .order_by(
                'user__first_name',
                'user__last_name'
            )
        )

        # --------------------------------------------------
        # RESEARCHER IDS
        # --------------------------------------------------

        researcher_ids = list(
            researchers.values_list(
                'user_id',
                flat=True
            )
        )

        # --------------------------------------------------
        # TECHNICIAN IDS
        # --------------------------------------------------

        technician_ids = list(
            technicians.values_list(
                'user_id',
                flat=True
            )
        )

        # --------------------------------------------------
        # ALL TEAM MEMBER IDS
        # --------------------------------------------------

        member_ids = (
            researcher_ids +
            technician_ids
        )

        # --------------------------------------------------
        # AVAILABLE CHEMICALS
        # --------------------------------------------------

        available_chemicals = (
            Chemical.objects
            .filter(
                researcher_id__in=member_ids,
                status='AVAILABLE'
            )
            .order_by(
                'name'
            )
        )

        # --------------------------------------------------
        # AVAILABLE EQUIPMENT
        # --------------------------------------------------

        available_equipment = (
            Equipment.objects
            .filter(
                researcher_id__in=member_ids,
                status='AVAILABLE'
            )
            .order_by(
                'name'
            )
        )

        # --------------------------------------------------
        # EXPERIMENTS DONE
        # --------------------------------------------------

        experiments_done = (
            Experiment.objects
            .filter(
                researcher_id__in=researcher_ids
            )
            .order_by(
                '-created_at'
            )
        )

        # --------------------------------------------------
        # RECENT ACTIVITIES FOR THIS BRANCH
        # --------------------------------------------------

        activities = list(
            LabActivity.objects
            .filter(
                actor_id__in=member_ids
            )
            .select_related('actor')
            .order_by(
                '-created_at'
            )[:15]
        )

        prepare_activities(
            activities
        )

        # --------------------------------------------------
        # SAVE BRANCH DATA
        # --------------------------------------------------

        sub_admin_data.append({

            'profile':
                sub_admin_profile,

            'user':
                sub_admin,

            'institution_name':
                institution_name,

            'researchers':
                researchers,

            'technicians':
                technicians,

            'activities':
                activities,

            'available_chemicals':
                available_chemicals,

            'available_equipment':
                available_equipment,

            'experiments_done':
                experiments_done,

            'total_researchers':
                researchers.count(),

            'total_technicians':
                technicians.count(),

            'total_available_chemicals':
                available_chemicals.count(),

            'total_available_equipment':
                available_equipment.count(),

            'total_experiments_done':
                experiments_done.count(),
        })

    # ------------------------------------------------------
    # ALL RECENT LABORATORY ACTIVITIES
    #
    # USER is kept separately from ACTIVITY.
    #
    # Example:
    #
    # User:
    #     shyam_technician
    #
    # Activity:
    #     Chemical
    #
    # NOT:
    #
    #     shyam_technician - CHEMICAL
    # ------------------------------------------------------

    recent_activities = list(
        LabActivity.objects
        .select_related('actor')
        .order_by(
            '-created_at'
        )[:15]
    )

    prepare_activities(
        recent_activities
    )

    # ------------------------------------------------------
    # CONTEXT
    # ------------------------------------------------------

    context = {

        'sub_admin_data':
            sub_admin_data,

        'total_sub_admins':
            total_sub_admins,

        'total_researchers':
            total_researchers,

        'total_technicians':
            total_technicians,

        'total_activities':
            total_activities,

        'recent_activities':
            recent_activities,
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

    # ------------------------------------------------------
    # GET CURRENT SUB-ADMIN PROFILE
    # ------------------------------------------------------

    profile = get_sub_admin_profile(
        request.user
    )

    # ------------------------------------------------------
    # IMPORTANT:
    # If the CustomUser is not a Sub-Administrator,
    # deny access.
    # ------------------------------------------------------

    if profile is None:

        return render(
            request,
            'sub_admin_dashboard.html',
            {
                'access_denied': True
            }
        )

    # ------------------------------------------------------
    # CURRENT INSTITUTION / COMPANY
    # ------------------------------------------------------

    institution_name = (
        get_user_institution(
            request.user
        )
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
        .order_by(
            'user__first_name',
            'user__last_name'
        )
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
        .order_by(
            'user__first_name',
            'user__last_name'
        )
    )

    # ------------------------------------------------------
    # RESEARCHER IDS
    # ------------------------------------------------------

    researcher_ids = list(
        researchers.values_list(
            'user_id',
            flat=True
        )
    )

    # ------------------------------------------------------
    # TECHNICIAN IDS
    # ------------------------------------------------------

    technician_ids = list(
        technicians.values_list(
            'user_id',
            flat=True
        )
    )

    # ------------------------------------------------------
    # ALL TEAM MEMBER IDS
    # ------------------------------------------------------

    member_ids = (
        researcher_ids +
        technician_ids
    )

    # ------------------------------------------------------
    # AVAILABLE CHEMICALS
    # ------------------------------------------------------

    available_chemicals = (
        Chemical.objects
        .filter(
            researcher_id__in=member_ids,
            status='AVAILABLE'
        )
        .order_by(
            'name'
        )
    )

    # ------------------------------------------------------
    # AVAILABLE EQUIPMENT
    # ------------------------------------------------------

    available_equipment = (
        Equipment.objects
        .filter(
            researcher_id__in=member_ids,
            status='AVAILABLE'
        )
        .order_by(
            'name'
        )
    )

    # ------------------------------------------------------
    # EXPERIMENTS DONE
    # ------------------------------------------------------

    experiments_done = (
        Experiment.objects
        .filter(
            researcher_id__in=researcher_ids
        )
        .order_by(
            '-created_at'
        )
    )

    # ------------------------------------------------------
    # RECENT TEAM ACTIVITIES
    # ------------------------------------------------------

    activities = list(
        LabActivity.objects
        .filter(
            actor_id__in=member_ids
        )
        .select_related('actor')
        .order_by(
            '-created_at'
        )[:15]
    )

    prepare_activities(
        activities
    )

    # ------------------------------------------------------
    # CONTEXT
    # ------------------------------------------------------

    context = {

        'profile':
            profile,

        'institution_name':
            institution_name,

        'researchers':
            researchers,

        'technicians':
            technicians,

        'activities':
            activities,

        'available_chemicals':
            available_chemicals,

        'available_equipment':
            available_equipment,

        'experiments_done':
            experiments_done,

        'total_researchers':
            researchers.count(),

        'total_technicians':
            technicians.count(),

        'total_available_chemicals':
            available_chemicals.count(),

        'total_available_equipment':
            available_equipment.count(),

        'total_experiments_done':
            experiments_done.count(),
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

    experiments = (
        Experiment.objects
        .filter(
            researcher=request.user
        )
        .order_by(
            '-created_at'
        )
    )

    activities = (
        LabActivity.objects
        .filter(
            actor=request.user
        )
        .order_by(
            '-created_at'
        )[:10]
    )

    return render(
        request,
        'researcher_dashboard.html',
        {
            'experiments':
                experiments,

            'activities':
                activities,
        }
    )


# ==========================================================
# TECHNICIAN DASHBOARD
# ==========================================================

@login_required
def technician_dashboard(request):

    activities = (
        LabActivity.objects
        .filter(
            actor=request.user,
            activity_type__in=[
                'EQUIPMENT',
                'MAINTENANCE',
                'CHEMICAL',
            ]
        )
        .select_related('actor')
        .order_by(
            '-created_at'
        )[:15]
    )

    return render(
        request,
        'technician_dashboard.html',
        {
            'activities':
                activities
        }
    )


# ==========================================================
# CREATE SUB-ADMINISTRATOR
# ==========================================================

@login_required
def create_sub_admin(request):

    # ------------------------------------------------------
    # CENTRAL ADMINISTRATOR ONLY
    # ------------------------------------------------------

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

        form = SubAdminForm(
            request.POST
        )

        if form.is_valid():

            # --------------------------------------------------
            # CREATE USER
            # --------------------------------------------------

            user = form.save()

            # --------------------------------------------------
            # INSTITUTION / COMPANY
            # --------------------------------------------------

            institution_name = (
                request.POST
                .get(
                    'institution',
                    ''
                )
                .strip()
            )

            # --------------------------------------------------
            # SAVE INSTITUTION
            # --------------------------------------------------

            if hasattr(
                user,
                'institution'
            ):

                user.institution = (
                    institution_name
                )

                user.save(
                    update_fields=[
                        'institution'
                    ]
                )

            # --------------------------------------------------
            # MAKE SURE CUSTOM USER ROLE IS SUB_ADMIN
            # --------------------------------------------------

            if hasattr(
                user,
                'role'
            ):

                user.role = 'SUB_ADMIN'

                user.save(
                    update_fields=[
                        'role'
                    ]
                )

            # --------------------------------------------------
            # CREATE / UPDATE LAB PROFILE
            # --------------------------------------------------

            LabProfile.objects.update_or_create(
                user=user,
                defaults={
                    'role':
                        'SUB_ADMIN',

                    'supervisor':
                        None,
                }
            )

            # --------------------------------------------------
            # RECORD ACTIVITY
            # --------------------------------------------------

            LabActivity.objects.create(
                actor=request.user,
                activity_type='OTHER',
                description=(
                    f'Created '
                    f'Sub-Administrator: '
                    f'{user.username}'
                )
            )

            # --------------------------------------------------
            # SUCCESS
            # --------------------------------------------------

            messages.success(
                request,
                f'Sub-Administrator '
                f'"{user.username}" '
                f'created successfully.'
            )

            return redirect(
                'dashboard'
            )

    else:

        form = SubAdminForm()

    # ------------------------------------------------------
    # DISPLAY FORM
    # ------------------------------------------------------

    return render(
        request,
        'create_sub_admin.html',
        {
            'form':
                form
        }
    )


# ==========================================================
# EDIT SUB-ADMINISTRATOR
# ==========================================================

@login_required
def edit_sub_admin(request, user_id):

    # ------------------------------------------------------
    # CENTRAL ADMINISTRATOR ONLY
    # ------------------------------------------------------

    if not request.user.is_superuser:

        return render(
            request,
            'edit_sub_admin.html',
            {
                'access_denied': True
            }
        )

    # ------------------------------------------------------
    # GET SUB-ADMIN
    # ------------------------------------------------------

    try:

        profile = (
            LabProfile.objects
            .select_related('user')
            .get(
                user_id=user_id,
                role='SUB_ADMIN'
            )
        )

    except LabProfile.DoesNotExist:

        messages.error(
            request,
            'Sub-Administrator not found.'
        )

        return redirect(
            'dashboard'
        )

    user = profile.user

    # ------------------------------------------------------
    # CURRENT INSTITUTION
    # ------------------------------------------------------

    institution_name = (
        get_user_institution(
            user
        )
    )

    # ------------------------------------------------------
    # POST
    # ------------------------------------------------------

    if request.method == 'POST':

        form = SubAdminForm(
            request.POST,
            instance=user
        )

        if form.is_valid():

            updated_user = (
                form.save()
            )

            # --------------------------------------------------
            # UPDATE INSTITUTION
            # --------------------------------------------------

            new_institution_name = (
                request.POST
                .get(
                    'institution',
                    ''
                )
                .strip()
            )

            if hasattr(
                updated_user,
                'institution'
            ):

                updated_user.institution = (
                    new_institution_name
                )

                updated_user.save(
                    update_fields=[
                        'institution'
                    ]
                )

            # --------------------------------------------------
            # MAKE SURE ROLE REMAINS SUB_ADMIN
            # --------------------------------------------------

            if hasattr(
                updated_user,
                'role'
            ):

                if updated_user.role != 'SUB_ADMIN':

                    updated_user.role = 'SUB_ADMIN'

                    updated_user.save(
                        update_fields=[
                            'role'
                        ]
                    )

            # --------------------------------------------------
            # RECORD ACTIVITY
            # --------------------------------------------------

            LabActivity.objects.create(
                actor=request.user,
                activity_type='OTHER',
                description=(
                    f'Updated '
                    f'Sub-Administrator: '
                    f'{updated_user.username}'
                )
            )

            messages.success(
                request,
                f'Sub-Administrator '
                f'"{updated_user.username}" '
                f'updated successfully.'
            )

            return redirect(
                'dashboard'
            )

    else:

        form = SubAdminForm(
            instance=user
        )

    # ------------------------------------------------------
    # DISPLAY FORM
    # ------------------------------------------------------

    return render(
        request,
        'edit_sub_admin.html',
        {
            'form':
                form,

            'profile':
                profile,

            'user':
                user,

            'institution_name':
                institution_name,
        }
    )


# ==========================================================
# DELETE SUB-ADMINISTRATOR
# ==========================================================

@login_required
def delete_sub_admin(request, user_id):

    # ------------------------------------------------------
    # CENTRAL ADMINISTRATOR ONLY
    # ------------------------------------------------------

    if not request.user.is_superuser:

        return render(
            request,
            'delete_sub_admin.html',
            {
                'access_denied': True
            }
        )

    # ------------------------------------------------------
    # ONLY POST
    # ------------------------------------------------------

    if request.method != 'POST':

        return redirect(
            'dashboard'
        )

    # ------------------------------------------------------
    # GET SUB-ADMIN
    # ------------------------------------------------------

    try:

        profile = (
            LabProfile.objects
            .select_related('user')
            .get(
                user_id=user_id,
                role='SUB_ADMIN'
            )
        )

    except LabProfile.DoesNotExist:

        messages.error(
            request,
            'Sub-Administrator not found.'
        )

        return redirect(
            'dashboard'
        )

    user = profile.user

    username = (
        user.username
    )

    institution_name = (
        get_user_institution(
            user
        )
    )

    # ------------------------------------------------------
    # RECORD ACTIVITY BEFORE DELETE
    # ------------------------------------------------------

    LabActivity.objects.create(
        actor=request.user,
        activity_type='OTHER',
        description=(
            f'Removed '
            f'Sub-Administrator: '
            f'{username}'
        )
    )

    # ------------------------------------------------------
    # DELETE
    # ------------------------------------------------------

    user.delete()

    # ------------------------------------------------------
    # SUCCESS
    # ------------------------------------------------------

    messages.success(
        request,
        f'Sub-Administrator '
        f'"{username}" '
        f'from '
        f'"{institution_name}" '
        f'removed successfully.'
    )

    return redirect(
        'dashboard'
    )


# ==========================================================
# CREATE RESEARCHER / TECHNICIAN
# ==========================================================

@login_required
def create_team_member(request):

    # ------------------------------------------------------
    # GET CURRENT SUB-ADMIN PROFILE
    # ------------------------------------------------------

    profile = get_sub_admin_profile(
        request.user
    )

    # ------------------------------------------------------
    # IMPORTANT FIX:
    #
    # Previously the code immediately returned
    # access_denied=True when LabProfile did not exist.
    #
    # Now get_sub_admin_profile() also checks:
    #
    # request.user.role == 'SUB_ADMIN'
    #
    # and creates the missing LabProfile automatically.
    # ------------------------------------------------------

    if profile is None:

        return render(
            request,
            'create_team_member.html',
            {
                'access_denied': True
            }
        )

    # ------------------------------------------------------
    # CURRENT INSTITUTION / COMPANY
    # ------------------------------------------------------

    institution_name = (
        get_user_institution(
            request.user
        )
    )

    # ------------------------------------------------------
    # POST
    # ------------------------------------------------------

    if request.method == 'POST':

        form = TeamMemberForm(
            request.POST
        )

        if form.is_valid():

            # --------------------------------------------------
            # CREATE USER
            # --------------------------------------------------

            user = form.save()

            # --------------------------------------------------
            # ROLE
            # --------------------------------------------------

            role = form.cleaned_data[
                'role'
            ]

            # --------------------------------------------------
            # ASSIGN INSTITUTION / COMPANY
            #
            # Team members belong to the current
            # Sub-Administrator's institution.
            # --------------------------------------------------

            if hasattr(
                user,
                'institution'
            ):

                user.institution = (
                    institution_name
                )

                user.save(
                    update_fields=[
                        'institution'
                    ]
                )

            # --------------------------------------------------
            # CREATE LAB PROFILE
            #
            # supervisor=request.user is what connects
            # the new member to this Sub-Administrator.
            # --------------------------------------------------

            LabProfile.objects.create(
                user=user,
                role=role,
                supervisor=request.user,
            )

            # --------------------------------------------------
            # ACTIVITY
            # --------------------------------------------------

            role_name = (
                'Researcher'
                if role == 'RESEARCHER'
                else 'Technician'
            )

            LabActivity.objects.create(
                actor=request.user,
                activity_type='OTHER',
                description=(
                    f'Created '
                    f'{role_name}: '
                    f'{user.username}'
                )
            )

            # --------------------------------------------------
            # SUCCESS
            # --------------------------------------------------

            messages.success(
                request,
                f'{user.username} '
                f'was created successfully.'
            )

            return redirect(
                'sub_admin_dashboard'
            )

    else:

        form = TeamMemberForm()

    # ------------------------------------------------------
    # DISPLAY FORM
    # ------------------------------------------------------

    return render(
        request,
        'create_team_member.html',
        {
            'form':
                form,

            'profile':
                profile,

            'institution_name':
                institution_name,
        }
    )


# ==========================================================
# EDIT RESEARCHER / TECHNICIAN
# ==========================================================

@login_required
def edit_team_member(request, user_id):

    # ------------------------------------------------------
    # SUB-ADMINISTRATOR ONLY
    # ------------------------------------------------------

    sub_admin_profile = (
        get_sub_admin_profile(
            request.user
        )
    )

    if sub_admin_profile is None:

        return render(
            request,
            'edit_team_member.html',
            {
                'access_denied': True
            }
        )

    # ------------------------------------------------------
    # GET MEMBER
    #
    # IMPORTANT:
    # supervisor=request.user prevents a Sub-Admin
    # from editing another laboratory's users.
    # ------------------------------------------------------

    try:

        profile = (
            LabProfile.objects
            .select_related('user')
            .get(
                user_id=user_id,
                supervisor=request.user,
                role__in=[
                    'RESEARCHER',
                    'TECHNICIAN'
                ]
            )
        )

    except LabProfile.DoesNotExist:

        messages.error(
            request,
            'Researcher/Technician not found.'
        )

        return redirect(
            'sub_admin_dashboard'
        )

    user = profile.user

    # ------------------------------------------------------
    # POST
    # ------------------------------------------------------

    if request.method == 'POST':

        form = TeamMemberForm(
            request.POST,
            instance=user
        )

        if form.is_valid():

            updated_user = (
                form.save()
            )

            # --------------------------------------------------
            # ENSURE INSTITUTION STAYS WITH CURRENT SUB-ADMIN
            # --------------------------------------------------

            institution_name = (
                get_user_institution(
                    request.user
                )
            )

            if hasattr(
                updated_user,
                'institution'
            ):

                updated_user.institution = (
                    institution_name
                )

                updated_user.save(
                    update_fields=[
                        'institution'
                    ]
                )

            # --------------------------------------------------
            # ROLE NAME
            # --------------------------------------------------

            role_name = (
                'Researcher'
                if profile.role == 'RESEARCHER'
                else 'Technician'
            )

            # --------------------------------------------------
            # ACTIVITY
            # --------------------------------------------------

            LabActivity.objects.create(
                actor=request.user,
                activity_type='OTHER',
                description=(
                    f'Updated '
                    f'{role_name}: '
                    f'{updated_user.username}'
                )
            )

            messages.success(
                request,
                f'{updated_user.username} '
                f'updated successfully.'
            )

            return redirect(
                'sub_admin_dashboard'
            )

    else:

        form = TeamMemberForm(
            instance=user
        )

    # ------------------------------------------------------
    # CURRENT INSTITUTION
    # ------------------------------------------------------

    institution_name = (
        get_user_institution(
            request.user
        )
    )

    return render(
        request,
        'edit_team_member.html',
        {
            'form':
                form,

            'profile':
                profile,

            'user':
                user,

            'institution_name':
                institution_name,
        }
    )


# ==========================================================
# DELETE RESEARCHER / TECHNICIAN
# ==========================================================

@login_required
def delete_team_member(request, user_id):

    # ------------------------------------------------------
    # SUB-ADMINISTRATOR ONLY
    # ------------------------------------------------------

    profile_check = (
        get_sub_admin_profile(
            request.user
        )
    )

    if profile_check is None:

        return redirect(
            'sub_admin_dashboard'
        )

    # ------------------------------------------------------
    # ONLY MEMBER OF CURRENT SUB-ADMIN
    # ------------------------------------------------------

    try:

        profile = (
            LabProfile.objects
            .select_related('user')
            .get(
                user_id=user_id,
                supervisor=request.user,
                role__in=[
                    'RESEARCHER',
                    'TECHNICIAN'
                ]
            )
        )

    except LabProfile.DoesNotExist:

        messages.error(
            request,
            'Researcher/Technician not found.'
        )

        return redirect(
            'sub_admin_dashboard'
        )

    user = profile.user

    username = (
        user.username
    )

    role_name = (
        'Researcher'
        if profile.role == 'RESEARCHER'
        else 'Technician'
    )

    # ------------------------------------------------------
    # POST = DELETE
    # ------------------------------------------------------

    if request.method == 'POST':

        # --------------------------------------------------
        # RECORD ACTIVITY BEFORE DELETE
        # --------------------------------------------------

        LabActivity.objects.create(
            actor=request.user,
            activity_type='OTHER',
            description=(
                f'Removed '
                f'{role_name}: '
                f'{username}'
            )
        )

        # --------------------------------------------------
        # DELETE USER
        # --------------------------------------------------

        user.delete()

        # --------------------------------------------------
        # SUCCESS
        # --------------------------------------------------

        messages.success(
            request,
            f'{role_name} '
            f'"{username}" '
            f'removed successfully.'
        )

        return redirect(
            'sub_admin_dashboard'
        )

    # ------------------------------------------------------
    # GET = CONFIRMATION PAGE
    # ------------------------------------------------------

    return render(
        request,
        'delete_team_member.html',
        {
            'user':
                user,

            'profile':
                profile
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
# RESEARCHER - REPORTS
# ==========================================================

@login_required
def reports(request):

    return render(
        request,
        'reports.html'
    )


# ==========================================================
# EQUIPMENT
# ==========================================================

@login_required
def equipment(request):

    return render(
        request,
        'equipment.html'
    )


# ==========================================================
# MAINTENANCE
# ==========================================================

@login_required
def maintenance(request):

    return render(
        request,
        'maintenance.html'
    )


# ==========================================================
# CHEMICALS
# ==========================================================

@login_required
def chemicals(request):

    return render(
        request,
        'chemicals.html'
    )


# ==========================================================
# REGISTRATION CHOICE
# ==========================================================

def registration_choice(request):

    return render(
        request,
        'registration_choice.html'
    )