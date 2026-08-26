from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Chemical
from .forms import ChemicalForm


# ======================================================
# CHEMICAL LIST
# ======================================================

@login_required
def chemical_list(request):

    chemicals = Chemical.objects.filter(
        researcher=request.user
    ).order_by('-created_at')

    return render(
        request,
        'chemicals.html',
        {
            'chemicals': chemicals,
        }
    )


# ======================================================
# CREATE CHEMICAL
# ======================================================

@login_required
def create_chemical(request):

    if request.method == 'POST':

        form = ChemicalForm(request.POST)

        if form.is_valid():

            chemical = form.save(
                commit=False
            )

            # Automatically assign logged-in researcher
            chemical.researcher = request.user

            chemical.save()

            messages.success(
                request,
                'Chemical registered successfully.'
            )

            return redirect('chemicals')

    else:

        form = ChemicalForm()

    return render(
        request,
        'create_chemical.html',
        {
            'form': form,
        }
    )


# ======================================================
# EDIT CHEMICAL
# ======================================================

@login_required
def edit_chemical(request, chemical_id):

    chemical = get_object_or_404(
        Chemical,
        id=chemical_id,
        researcher=request.user
    )

    if request.method == 'POST':

        form = ChemicalForm(
            request.POST,
            instance=chemical
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Chemical updated successfully.'
            )

            return redirect('chemicals')

    else:

        form = ChemicalForm(
            instance=chemical
        )

    return render(
        request,
        'edit_chemical.html',
        {
            'form': form,
            'chemical': chemical,
        }
    )


# ======================================================
# DELETE CHEMICAL
# ======================================================

@login_required
def delete_chemical(request, chemical_id):

    chemical = get_object_or_404(
        Chemical,
        id=chemical_id,
        researcher=request.user
    )

    if request.method == 'POST':

        chemical.delete()

        messages.success(
            request,
            'Chemical removed successfully.'
        )

        return redirect('chemicals')

    return render(
        request,
        'remove_chemical.html',
        {
            'chemical': chemical,
        }
    )
