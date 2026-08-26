from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from accounts.models import CustomUser

from .forms import ExternalRegistrationForm
from .models import ExternalOrder, EquipmentBooking


def external_register(request):

    # If an external user is already logged in,
    # take them to their dashboard.
    if (
        request.user.is_authenticated
        and request.user.role == 'EXTERNAL'
    ):
        return redirect('external_dashboard')


    if request.method == 'POST':

        form = ExternalRegistrationForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            user.set_password(
                form.cleaned_data['password']
            )

            # Automatically assign External role
            user.role = 'EXTERNAL'

            # Teacher / Student / Other
            user.external_type = (
                form.cleaned_data['external_type']
            )

            user.save()

            # Log in newly created external user
            login(
                request,
                user
            )

            messages.success(
                request,
                'Your external account has been created successfully.'
            )

            return redirect(
                'external_dashboard'
            )

    else:

        form = ExternalRegistrationForm()


    return render(
        request,
        'external_register.html',
        {
            'form': form
        }
    )
# ======================================================
# EXTERNAL DASHBOARD
# ======================================================

@login_required
def external_dashboard(request):

    # Security check
    if request.user.role != 'EXTERNAL':

        messages.error(
            request,
            'You do not have permission to access the external dashboard.'
        )

        return redirect('home')

    orders = ExternalOrder.objects.filter(
        user=request.user
    ).order_by(
        '-created_at'
    )

    bookings = EquipmentBooking.objects.filter(
        user=request.user
    ).select_related(
        'equipment'
    ).order_by(
        '-booking_date'
    )

    return render(
        request,
        'external_dashboard.html',
        {
            'profile': request.user,
            'orders': orders,
            'bookings': bookings,
        }
    )


# ======================================================
# CHEMICALS
# ======================================================

@login_required
def external_chemicals(request):

    if request.user.role != 'EXTERNAL':
        return redirect('home')

    return render(
        request,
        'external_chemicals.html'
    )


# ======================================================
# EQUIPMENT
# ======================================================

@login_required
def external_equipment(request):

    if request.user.role != 'EXTERNAL':
        return redirect('home')

    from equipment.models import Equipment

    equipment = Equipment.objects.filter(
        status='AVAILABLE'
    ).order_by(
        'name'
    )

    return render(
        request,
        'external_equipment.html',
        {
            'equipment': equipment
        }
    )


# ======================================================
# EQUIPMENT BOOKING
# ======================================================

@login_required
def external_equipment_booking(request):

    if request.user.role != 'EXTERNAL':
        return redirect('home')

    from equipment.models import Equipment

    equipment = Equipment.objects.filter(
        status='AVAILABLE'
    ).order_by('name')

    return render(
        request,
        'external_equipment_booking.html',
        {'equipment': equipment}
    )


# ======================================================
# REPORTS
# ======================================================

@login_required
def external_reports(request):

    if request.user.role != 'EXTERNAL':
        return redirect('home')

    return render(
        request,
        'external_reports.html'
    )

# ======================================================
# LABORATORY REPORTS
# ======================================================

@login_required
def external_laboratory_reports(request):

    if request.user.role != 'EXTERNAL':
        return redirect('home')

    return render(
        request,
        'external_laboratory_reports.html'
    )


# ======================================================
# BOOKING REPORTS
# ======================================================

@login_required
def external_booking_reports(request):

    if request.user.role != 'EXTERNAL':
        return redirect('home')

    bookings = EquipmentBooking.objects.filter(
        user=request.user
    ).select_related(
        'equipment'
    ).order_by(
        '-booking_date'
    )

    return render(
        request,
        'external_booking_reports.html',
        {
            'bookings': bookings
        }
    )