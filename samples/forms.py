from django import forms
from .models import Sample


class SampleForm(forms.ModelForm):

    class Meta:

        model = Sample

        fields = [
            'name',
            'sample_code',
            'description',
            'collection_date',
            'status',
        ]

        widgets = {

            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter sample name'
                }
            ),

            'sample_code': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter sample code'
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Enter sample description'
                }
            ),

            'collection_date': forms.DateInput(
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