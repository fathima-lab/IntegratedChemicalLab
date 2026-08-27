from django import forms
from .models import Sample


class SampleForm(forms.ModelForm):

    class Meta:
        model = Sample

        fields = [
            'name',
            'sample_code',
            'description',
            'quantity',
            'unit',
            'storage_condition',
            'collection_date',
            'status',
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter sample name',
            }),

            'sample_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter sample code',
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter sample description',
                'rows': 4,
            }),

            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter quantity',
                'step': 'any',
                'min': '0',
            }),

            'unit': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. mL, g, kg',
            }),

            'storage_condition': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Room temperature, 4°C, -20°C',
            }),

            'collection_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),

            'status': forms.Select(attrs={
                'class': 'form-select',
            }),
        }