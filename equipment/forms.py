from django import forms
from .models import Equipment, Maintenance


class EquipmentForm(forms.ModelForm):

    class Meta:
        model = Equipment

        fields = [
            'name',
            'equipment_id',
            'description',
            'manufacturer',
            'model_number',
            'location',
            'status',
            'purchase_date',
            'last_maintenance',
            'next_maintenance',
        ]

        widgets = {

            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter equipment name'
                }
            ),

            'equipment_id': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter equipment ID'
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Enter equipment description'
                }
            ),

            'manufacturer': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter manufacturer'
                }
            ),

            'model_number': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter model number'
                }
            ),

            'location': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Example: Chemistry Laboratory'
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

            'last_maintenance': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),

            'next_maintenance': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),
        }

        labels = {
            'name': 'Equipment Name',
            'equipment_id': 'Equipment ID',
            'description': 'Description',
            'manufacturer': 'Manufacturer',
            'model_number': 'Model Number',
            'location': 'Location',
            'status': 'Status',
            'purchase_date': 'Purchase Date',
            'last_maintenance': 'Last Maintenance',
            'next_maintenance': 'Next Maintenance',
        }


# ======================================================
# MAINTENANCE FORM
# ======================================================

class MaintenanceForm(forms.ModelForm):

    class Meta:

        model = Maintenance

        fields = [
            'maintenance_type',
            'scheduled_date',
            'description',
            'status',
            'notes',
        ]

        widgets = {

            'maintenance_type': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'scheduled_date': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Describe the maintenance required'
                }
            ),

            'status': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'notes': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Enter additional maintenance notes'
                }
            ),
        }

        labels = {
            'maintenance_type': 'Maintenance Type',
            'scheduled_date': 'Scheduled Date',
            'description': 'Maintenance Description',
            'status': 'Maintenance Status',
            'notes': 'Additional Notes',
        }