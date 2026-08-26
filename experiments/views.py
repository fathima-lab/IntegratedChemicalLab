from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Experiment
from .forms import ExperimentForm
from dashboard.models import LabActivity


# ==========================================================
# EXPERIMENT LIST
# ==========================================================

@login_required
def experiments(request):

    experiments = Experiment.objects.filter(
        researcher=request.user
    ).order_by('-created_at')

    return render(
        request,
        'experiments.html',
        {
            'experiments': experiments
        }
    )


# ==========================================================
# CREATE EXPERIMENT
# ==========================================================

@login_required
def create_experiment(request):

    if request.method == 'POST':

        form = ExperimentForm(request.POST)

        if form.is_valid():

            # Create experiment without saving first
            experiment = form.save(commit=False)

            # Assign the logged-in researcher
            experiment.researcher = request.user

            # Save experiment
            experiment.save()

            # Record researcher activity
            LabActivity.objects.create(
                actor=request.user,
                activity_type='EXPERIMENT',
                description=f'Created experiment: {experiment.name}'
            )

            messages.success(
                request,
                'Experiment created successfully.'
            )

            return redirect('experiments')

    else:

        form = ExperimentForm()

    return render(
        request,
        'create_experiment.html',
        {
            'form': form
        }
    )

# ==========================================================
# VIEW EXPERIMENT
# ==========================================================

@login_required
def view_experiment(request, experiment_id):

    experiment = get_object_or_404(
        Experiment,
        id=experiment_id,
        researcher=request.user
    )

    return render(
        request,
        'view_experiment.html',
        {
            'experiment': experiment
        }
    )
# ==========================================================
# EDIT EXPERIMENT
# ==========================================================

@login_required
def edit_experiment(request, experiment_id):

    experiment = get_object_or_404(
        Experiment,
        id=experiment_id,
        researcher=request.user
    )

    if request.method == 'POST':

        form = ExperimentForm(
            request.POST,
            instance=experiment
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Experiment updated successfully.'
            )

            return redirect('experiments')

    else:

        form = ExperimentForm(
            instance=experiment
        )

    return render(
        request,
        'edit_experiment.html',
        {
            'form': form,
            'experiment': experiment
        }
    )


# ==========================================================
# DELETE EXPERIMENT
# ==========================================================

@login_required
def delete_experiment(request, experiment_id):

    experiment = get_object_or_404(
        Experiment,
        id=experiment_id,
        researcher=request.user
    )

    if request.method == 'POST':

        experiment_name = experiment.name

        experiment.delete()

        messages.success(
            request,
            f'Experiment "{experiment_name}" removed successfully.'
        )

        return redirect('experiments')

    return render(
        request,
        'delete_experiment.html',
        {
            'experiment': experiment
        }
    )