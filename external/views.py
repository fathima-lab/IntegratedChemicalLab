from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import CustomUser

from .forms import ExternalRegistrationForm
from .models import ExternalOrder, EquipmentBooking


# ======================================================
# EXTERNAL REGISTRATION
# ======================================================

def external_register(request):

    # If an external user is already logged in,
    # take them directly to their dashboard.
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


    # --------------------------------------------------
    # External user's chemical orders
    # --------------------------------------------------

    orders = (
        ExternalOrder.objects
        .filter(
            user=request.user
        )
        .order_by(
            '-created_at'
        )
    )


    # --------------------------------------------------
    # External user's equipment bookings
    # --------------------------------------------------

    bookings = (
        EquipmentBooking.objects
        .filter(
            user=request.user
        )
        .select_related(
            'equipment'
        )
        .order_by(
            '-booking_date',
            '-start_time'
        )
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

    # Security check
    if request.user.role != 'EXTERNAL':

        messages.error(
            request,
            'You do not have permission to access this page.'
        )

        return redirect('home')


    # --------------------------------------------------
    # Import Chemical model
    # --------------------------------------------------

    from chemicals.models import Chemical


    # --------------------------------------------------
    # Get available chemicals
    # --------------------------------------------------

    chemicals = (
        Chemical.objects
        .filter(
            status='AVAILABLE'
        )
        .order_by(
            'name'
        )
    )


    return render(
        request,
        'external_chemicals.html',
        {
            'chemicals': chemicals
        }
    )


# ======================================================
# CHEMICAL PURCHASE
# ======================================================

@login_required
def chemical_purchase(request, chemical_id):

    # Only external users can access this page
    if request.user.role != 'EXTERNAL':

        messages.error(
            request,
            'You do not have permission to access this page.'
        )

        return redirect('home')


    from chemicals.models import Chemical


    # --------------------------------------------------
    # Get selected chemical
    # --------------------------------------------------

    chemical = get_object_or_404(
        Chemical,
        id=chemical_id
    )


    # ==================================================
    # PLACE PURCHASE ORDER
    # ==================================================

    if request.method == 'POST':

        quantity = request.POST.get(
            'quantity'
        )


        # --------------------------------------------------
        # Validate quantity
        # --------------------------------------------------

        if not quantity:

            messages.error(
                request,
                'Please enter a quantity.'
            )

            return redirect(
                'chemical_purchase',
                chemical_id=chemical.id
            )


        try:

            quantity = Decimal(
                quantity
            )

        except (
            InvalidOperation,
            TypeError,
            ValueError
        ):

            messages.error(
                request,
                'Please enter a valid quantity.'
            )

            return redirect(
                'chemical_purchase',
                chemical_id=chemical.id
            )


        # --------------------------------------------------
        # Quantity must be positive
        # --------------------------------------------------

        if quantity <= 0:

            messages.error(
                request,
                'Quantity must be greater than zero.'
            )

            return redirect(
                'chemical_purchase',
                chemical_id=chemical.id
            )


        # --------------------------------------------------
        # Check available quantity
        # --------------------------------------------------

        chemical_quantity = getattr(
            chemical,
            'quantity',
            None
        )


        if chemical_quantity is not None:

            try:

                available_quantity = Decimal(
                    str(chemical_quantity)
                )


                if quantity > available_quantity:

                    unit = getattr(
                        chemical,
                        'unit',
                        ''
                    )


                    messages.error(
                        request,
                        f'Only {available_quantity:g} '
                        f'{unit} of {chemical.name} '
                        f'is available.'
                    )


                    return redirect(
                        'chemical_purchase',
                        chemical_id=chemical.id
                    )


            except (
                InvalidOperation,
                TypeError,
                ValueError
            ):

                pass


        # --------------------------------------------------
        # Chemical model has no price field.
        # Amount is therefore set to 0.00.
        # --------------------------------------------------

        amount = Decimal(
            '0.00'
        )


        # --------------------------------------------------
        # Chemical information
        # --------------------------------------------------

        chemical_code = getattr(
            chemical,
            'chemical_id',
            ''
        )


        unit = getattr(
            chemical,
            'unit',
            ''
        )


        # --------------------------------------------------
        # Build order description
        # --------------------------------------------------

        description = (
            f'Chemical: {chemical.name}'
        )


        if chemical_code:

            description += (
                f' | Chemical ID: {chemical_code}'
            )


        description += (
            f' | Quantity: {quantity:g} {unit}'
        )


        # --------------------------------------------------
        # Create purchase order
        # --------------------------------------------------

        ExternalOrder.objects.create(

            user=request.user,

            order_type='CHEMICAL',

            description=description,

            amount=amount,

            status='PENDING'

        )


        # --------------------------------------------------
        # Success message
        # --------------------------------------------------

        messages.success(
            request,
            f'Purchase request for '
            f'{quantity:g} {unit} of '
            f'{chemical.name} has been submitted successfully.'
        )


        return redirect(
            'external_dashboard'
        )


    # ==================================================
    # PURCHASE PAGE
    # ==================================================

    return render(
        request,
        'chemical_purchase.html',
        {
            'chemical': chemical
        }
    )


# ======================================================
# EQUIPMENT
# ======================================================

@login_required
def external_equipment(request):

    # Security check
    if request.user.role != 'EXTERNAL':

        messages.error(
            request,
            'You do not have permission to access this page.'
        )

        return redirect('home')


    from equipment.models import Equipment


    # --------------------------------------------------
    # Only available equipment is displayed
    # --------------------------------------------------

    equipment = (
        Equipment.objects
        .filter(
            status='AVAILABLE'
        )
        .order_by(
            'name'
        )
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
def external_equipment_booking(request, equipment_id):

    # --------------------------------------------------
    # SECURITY CHECK
    # --------------------------------------------------

    if request.user.role != 'EXTERNAL':

        messages.error(
            request,
            'You do not have permission to book equipment.'
        )

        return redirect('home')


    from equipment.models import Equipment


    # --------------------------------------------------
    # GET SELECTED EQUIPMENT
    # --------------------------------------------------

    equipment = get_object_or_404(
        Equipment,
        id=equipment_id
    )


    # --------------------------------------------------
    # CHECK EQUIPMENT AVAILABILITY
    # --------------------------------------------------

    if equipment.status != 'AVAILABLE':

        messages.error(
            request,
            'This equipment is currently unavailable.'
        )

        return redirect(
            'external_equipment'
        )


    # ==================================================
    # POST REQUEST
    # ==================================================

    if request.method == 'POST':

        booking_date = request.POST.get(
            'booking_date'
        )

        start_time = request.POST.get(
            'start_time'
        )

        end_time = request.POST.get(
            'end_time'
        )


        # --------------------------------------------------
        # VALIDATE BOOKING DATE
        # --------------------------------------------------

        if not booking_date:

            messages.error(
                request,
                'Please select a booking date.'
            )

            return render(
                request,
                'external_equipment_booking.html',
                {
                    'equipment': equipment,
                    'booking_date': booking_date,
                    'start_time': start_time,
                    'end_time': end_time,
                }
            )


        # --------------------------------------------------
        # VALIDATE START TIME
        # --------------------------------------------------

        if not start_time:

            messages.error(
                request,
                'Please select a start time.'
            )

            return render(
                request,
                'external_equipment_booking.html',
                {
                    'equipment': equipment,
                    'booking_date': booking_date,
                    'start_time': start_time,
                    'end_time': end_time,
                }
            )


        # --------------------------------------------------
        # VALIDATE END TIME
        # --------------------------------------------------

        if not end_time:

            messages.error(
                request,
                'Please select an end time.'
            )

            return render(
                request,
                'external_equipment_booking.html',
                {
                    'equipment': equipment,
                    'booking_date': booking_date,
                    'start_time': start_time,
                    'end_time': end_time,
                }
            )


        # --------------------------------------------------
        # VALIDATE TIME ORDER
        # --------------------------------------------------

        if start_time >= end_time:

            messages.error(
                request,
                'End time must be later than start time.'
            )

            return render(
                request,
                'external_equipment_booking.html',
                {
                    'equipment': equipment,
                    'booking_date': booking_date,
                    'start_time': start_time,
                    'end_time': end_time,
                }
            )


        # ==================================================
        # CREATE EQUIPMENT BOOKING
        # ==================================================

        EquipmentBooking.objects.create(
            user=request.user,
            equipment=equipment,
            booking_date=booking_date,
            start_time=start_time,
            end_time=end_time,
            amount=Decimal('0.00'),
            status='PENDING'
        )




        # ==================================================
        # SUCCESS MESSAGE
        # ==================================================

        messages.success(
            request,
            f'Booking request for {equipment.name} '
            f'has been submitted successfully.'
        )


        return redirect(
            'external_booking_reports'
        )


    # ==================================================
    # GET REQUEST
    # ==================================================

    return render(
        request,
        'external_equipment_booking.html',
        {
            'equipment': equipment
        }
    )

# ======================================================
# BOOKING REPORTS
# ======================================================

@login_required
def external_booking_reports(request):

    # Security check
    if request.user.role != 'EXTERNAL':

        messages.error(
            request,
            'You do not have permission to access this page.'
        )

        return redirect('home')

    # Get bookings made by the logged-in external user
    bookings = (
        EquipmentBooking.objects
        .filter(
            user=request.user
        )
        .select_related(
            'equipment'
        )
        .order_by(
            '-booking_date'
        )
    )

    return render(
        request,
        'external_booking_reports.html',
        {
            'bookings': bookings
        }
    )

