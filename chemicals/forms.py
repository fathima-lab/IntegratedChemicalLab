from django import forms
from .models import Chemical


class ChemicalForm(forms.ModelForm):

    class Meta:
        model = Chemical

        fields = [
            'name',
            'chemical_id',
            'formula',
            'cas_number',
            'description',
            'quantity',
            'unit',
            'storage_location',
            'hazard_information',
            'status',
            'purchase_date',
            'expiry_date',
        ]

        widgets = {

            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter chemical name'
                }
            ),

            'chemical_id': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter chemical ID'
                }
            ),

            'formula': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Example: H₂SO₄'
                }
            ),

            'cas_number': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter CAS number'
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Enter chemical description'
                }
            ),

            'quantity': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'step': '0.001',
                    'min': '0',
                    'placeholder': 'Enter quantity'
                }
            ),

            'unit': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Example: g, kg, mL, L'
                }
            ),

            'storage_location': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Example: Chemical Storage Room A'
                }
            ),

            'hazard_information': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Enter hazard and safety information'
                }
            ),

            'status': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'purchase_date': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),

            'expiry_date': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),
        }

        labels = {
            'name': 'Chemical Name',
            'chemical_id': 'Chemical ID',
            'formula': 'Chemical Formula',
            'cas_number': 'CAS Number',
            'description': 'Description',
            'quantity': 'Quantity',
            'unit': 'Unit',
            'storage_location': 'Storage Location',
            'hazard_information': 'Hazard & Safety Information',
            'status': 'Status',
            'purchase_date': 'Purchase Date',
            'expiry_date': 'Expiry Date',
        }