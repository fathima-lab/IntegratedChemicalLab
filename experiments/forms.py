from django import forms
from .models import Experiment


class ExperimentForm(forms.ModelForm):

    class Meta:
        model = Experiment

        fields = [
            'name',
            'description',
            'results_observations',
            'conclusion',
            'start_date',
            'end_date',
            'status',
        ]

        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter experiment name'
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Enter experiment description'
                }
            ),
            'results_observations': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 6,
                    'placeholder': 'Enter experimental results, measurements and observations'
                }
            ),

            'conclusion': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 5,
                    'placeholder': 'Enter the conclusion drawn from the experiment'
                }
            ),

            'start_date': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),

            'end_date': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),

            'status': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),
        }