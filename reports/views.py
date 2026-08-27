from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Report
from .forms import ReportForm
from dashboard.models import LabActivity

# ======================================================
# REPORTS LIST
# ======================================================

@login_required
def reports(request):

    # Show only reports created by the logged-in researcher
    user_reports = Report.objects.filter(
        researcher=request.user
    ).select_related(
        'experiment'
    )

    return render(
        request,
        'reports.html',
        {
            'reports': user_reports,
        }
    )


# ======================================================
# CREATE REPORT
# ======================================================

@login_required
def create_report(request):

    if request.method == 'POST':

        form = ReportForm(
            request.POST
        )

        if form.is_valid():

            report = form.save(
                commit=False
            )

            # Automatically assign logged-in researcher
            report.researcher = request.user

            report.save()

            # Record report activity
            LabActivity.objects.create(
                actor=request.user,
                activity_type='REPORT',
                description=f'Created report: {report.title}'
            )

            messages.success(
                request,
                'Report created successfully.'
            )

            return redirect(
                'reports'
            )

    else:

        form = ReportForm()


    return render(
        request,
        'create_report.html',
        {
            'form': form,
        }
    )


# ======================================================
# EDIT REPORT
# ======================================================

@login_required
def edit_report(request, report_id):

    report = get_object_or_404(
        Report,
        id=report_id,
        researcher=request.user
    )

    if request.method == 'POST':

        form = ReportForm(
            request.POST,
            instance=report
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Report updated successfully.'
            )

            return redirect(
                'reports'
            )

    else:

        form = ReportForm(
            instance=report
        )


    return render(
        request,
        'edit_report.html',
        {
            'form': form,
            'report': report,
        }
    )


# ======================================================
# DELETE REPORT
# ======================================================

@login_required
def delete_report(request, report_id):

    report = get_object_or_404(
        Report,
        id=report_id,
        researcher=request.user
    )

    if request.method == 'POST':

        report.delete()

        messages.success(
            request,
            'Report removed successfully.'
        )

        return redirect(
            'reports'
        )


    return render(
        request,
        'delete_report.html',
        {
            'report': report,
        }
    )