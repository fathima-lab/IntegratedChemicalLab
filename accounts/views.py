from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import RegisterForm
from dashboard.models import LabProfile


# ==========================================================
# LOGIN
# ==========================================================

def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            # ------------------------------------------------
            # CENTRAL ADMINISTRATOR
            # ------------------------------------------------

            if user.is_superuser:
                return redirect('dashboard')

            # ------------------------------------------------
            # OTHER USERS
            # ------------------------------------------------

            try:

                profile = user.lab_profile

                if profile.role == 'SUB_ADMIN':
                    return redirect('sub_admin_dashboard')

                elif profile.role == 'RESEARCHER':
                    return redirect('researcher_dashboard')

                elif profile.role == 'TECHNICIAN':
                    return redirect('technician_dashboard')

            except LabProfile.DoesNotExist:
                pass

            return redirect('home')

        return render(
            request,
            'login.html',
            {
                'error': 'Invalid username or password.'
            }
        )

    return render(
        request,
        'login.html'
    )


# ==========================================================
# REGISTER
# ==========================================================

def register(request):

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            # ------------------------------------------------
            # SAVE USER ACCOUNT
            # ------------------------------------------------

            user = form.save()

            # ------------------------------------------------
            # GET ROLE FROM FORM
            #
            # IMPORTANT:
            # role is NOT stored in CustomUser.
            # It is stored in LabProfile.
            # ------------------------------------------------

            role = form.cleaned_data.get('role')

            supervisor = form.cleaned_data.get('supervisor')

            # ------------------------------------------------
            # CENTRAL ADMINISTRATOR
            # ------------------------------------------------

            if role == 'CENTRAL_ADMIN':

                user.is_staff = True
                user.is_superuser = True
                user.save()

                # Central Administrator does not need
                # a LabProfile.

                messages.success(
                    request,
                    'Central Administrator created successfully.'
                )

                login(request, user)

                return redirect('dashboard')

            # ------------------------------------------------
            # SUB ADMIN / RESEARCHER / TECHNICIAN
            # ------------------------------------------------

            LabProfile.objects.create(
                user=user,
                role=role,
                supervisor=supervisor,
                phone=form.cleaned_data.get('phone', '')
            )

            # ------------------------------------------------
            # LOGIN NEW USER
            # ------------------------------------------------

            login(request, user)

            # ------------------------------------------------
            # REDIRECT BASED ON ROLE
            # ------------------------------------------------

            if role == 'SUB_ADMIN':

                return redirect(
                    'sub_admin_dashboard'
                )

            elif role == 'RESEARCHER':

                return redirect(
                    'researcher_dashboard'
                )

            elif role == 'TECHNICIAN':

                return redirect(
                    'technician_dashboard'
                )

            return redirect('home')

    else:

        form = RegisterForm()

    return render(
        request,
        'register.html',
        {
            'form': form
        }
    )


# ==========================================================
# LOGOUT
# ==========================================================

def logout_view(request):

    logout(request)

    return redirect('home')