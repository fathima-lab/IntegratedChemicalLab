from django import forms
from .models import Report
from experiments.models import Experiment


class ReportForm(forms.ModelForm):

    class Meta:
        model = Report

        fields = [
            'experiment',
            'title',
            'report_date',
            'observations',
            'results',
            'conclusion',
        ]

        widgets = {
            'experiment': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter report title'
                }
            ),

            'report_date': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),

            'observations': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 5,
                    'placeholder': 'Enter observations obtained during the experiment'
                }
            ),

            'results': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 5,
                    'placeholder': 'Enter the results obtained'
                }
            ),

            'conclusion': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 5,
                    'placeholder': 'Enter the final conclusion'
                }
            ),
        }

        labels = {
            'experiment': 'Experiment',
            'title': 'Report Title',
            'report_date': 'Report Date',
            'observations': 'Observations',
            'results': 'Results Obtained',
            'conclusion': 'Conclusion',
        }

    def __init__(self, *args, **kwargs):

        researcher = kwargs.pop(
            'researcher',
            None
        )

        super().__init__(*args, **kwargs)

        if researcher:

            self.fields['experiment'].queryset = Experiment.objects.filter(
                researcher=researcher
            )