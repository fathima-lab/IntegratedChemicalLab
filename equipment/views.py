from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Equipment, Maintenance
from .forms import EquipmentForm, MaintenanceForm
from dashboard.models import LabActivity


# ======================================================
# EQUIPMENT LIST
# ======================================================

@login_required
def equipment_list(request):

    equipment = Equipment.objects.filter(
        researcher=request.user
    ).order_by('-created_at')

    return render(
        request,
        'equipment.html',
        {
            'equipment': equipment,
        }
    )


# ======================================================
# CREATE EQUIPMENT
# ======================================================

@login_required
def create_equipment(request):

    if request.method == 'POST':

        form = EquipmentForm(request.POST)

        if form.is_valid():

            equipment = form.save(
                commit=False
            )

            # Assign logged-in researcher
            equipment.researcher = request.user

            equipment.save()

            # Record equipment activity
            LabActivity.objects.create(
                actor=request.user,
                activity_type='EQUIPMENT',
                description=f'Equipment registered: {equipment.name}'
            )

            messages.success(
                request,
                'Equipment registered successfully.'
            )

            return redirect('equipment')

    else:

        form = EquipmentForm()

    return render(
        request,
        'create_equipment.html',
        {
            'form': form,
        }
    )


# ======================================================
# UPDATE EQUIPMENT
# ======================================================

@login_required
def update_equipment(request, equipment_id):

    equipment = get_object_or_404(
        Equipment,
        id=equipment_id,
        researcher=request.user
    )

    if request.method == 'POST':

        form = EquipmentForm(
            request.POST,
            instance=equipment
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Equipment updated successfully.'
            )

            return redirect('equipment')

    else:

        form = EquipmentForm(
            instance=equipment
        )

    return render(
        request,
        'update_equipment.html',
        {
            'form': form,
            'equipment': equipment,
        }
    )


# ======================================================
# REMOVE EQUIPMENT
# ======================================================

@login_required
def remove_equipment(request, equipment_id):

    equipment = get_object_or_404(
        Equipment,
        id=equipment_id,
        researcher=request.user
    )

    if request.method == 'POST':

        equipment.delete()

        messages.success(
            request,
            'Equipment removed successfully.'
        )

        return redirect('equipment')

    return render(
        request,
        'remove_equipment.html',
        {
            'equipment': equipment,
        }
    )

@login_required
def maintenance(request):

    equipment = Equipment.objects.filter(
        researcher=request.user
    ).order_by('name')


    maintenance_records = Maintenance.objects.filter(
        equipment__researcher=request.user
    ).select_related(
        'equipment',
        'scheduled_by'
    ).order_by(
        '-scheduled_date'
    )


    total_maintenance = maintenance_records.count()

    scheduled_maintenance = maintenance_records.filter(
        status='SCHEDULED'
    ).count()

    completed_maintenance = maintenance_records.filter(
        status='COMPLETED'
    ).count()


    return render(
        request,
        'maintenance.html',
        {
            'equipment': equipment,

            'maintenance_records':
                maintenance_records,

            'total_maintenance':
                total_maintenance,

            'scheduled_maintenance':
                scheduled_maintenance,

            'completed_maintenance':
                completed_maintenance,
        }
    )
@login_required
def schedule_maintenance(request, equipment_id):

    equipment = get_object_or_404(
        Equipment,
        id=equipment_id,
        researcher=request.user
    )

    if request.method == 'POST':

        form = MaintenanceForm(request.POST)

        if form.is_valid():

            maintenance = form.save(
                commit=False
            )

            maintenance.equipment = equipment
            maintenance.scheduled_by = request.user

            maintenance.save()

            # Record maintenance activity
            LabActivity.objects.create(
                actor=request.user,
                activity_type='MAINTENANCE',
                description=f'Maintenance scheduled for {equipment.name}'
            )

            messages.success(
                request,
                'Maintenance scheduled successfully.'
            )

            return redirect('maintenance')

    else:

        form = MaintenanceForm()

    return render(
        request,
        'schedule_maintenance.html',
        {
            'form': form,
            'equipment': equipment,
        }
    )