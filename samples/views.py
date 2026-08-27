from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Sample
from .forms import SampleForm

from dashboard.models import LabActivity


# ==========================================================
# SAMPLE LIST
# ==========================================================

@login_required
def samples(request):

    samples = Sample.objects.filter(
        researcher=request.user
    ).order_by('-created_at')

    return render(
        request,
        'samples.html',
        {
            'samples': samples
        }
    )


# ==========================================================
# CREATE SAMPLE
# ==========================================================

@login_required
def create_sample(request):

    if request.method == 'POST':

        form = SampleForm(request.POST)

        if form.is_valid():

            sample = form.save(commit=False)

            sample.researcher = request.user

            sample.save()

            # Record sample activity
            LabActivity.objects.create(
                actor=request.user,
                activity_type='SAMPLE',
                description=f'Created sample: {sample.name}'
            )

            messages.success(
                request,
                'Sample created successfully.'
            )

            return redirect('samples')

    else:

        form = SampleForm()

    return render(
        request,
        'create_sample.html',
        {
            'form': form
        }
    )


# ==========================================================
# EDIT SAMPLE
# ==========================================================

@login_required
def edit_sample(request, sample_id):

    sample = get_object_or_404(
        Sample,
        id=sample_id,
        researcher=request.user
    )

    if request.method == 'POST':

        form = SampleForm(
            request.POST,
            instance=sample
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Sample updated successfully.'
            )

            return redirect('samples')

    else:

        form = SampleForm(
            instance=sample
        )

    return render(
        request,
        'edit_samples.html',
        {
            'form': form,
            'sample': sample
        }
    )


# ==========================================================
# DELETE SAMPLE
# ==========================================================

@login_required
def delete_sample(request, sample_id):

    sample = get_object_or_404(
        Sample,
        id=sample_id,
        researcher=request.user
    )

    if request.method == 'POST':

        sample_name = sample.name

        sample.delete()

        messages.success(
            request,
            f'Sample "{sample_name}" removed successfully.'
        )

        return redirect('samples')

    return render(
        request,
        'delete_samples.html',
        {
            'sample': sample
        }
    )