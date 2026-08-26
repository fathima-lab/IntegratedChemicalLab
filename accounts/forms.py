from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.db.models import Q

from dashboard.models import LabProfile


User = get_user_model()


class RegisterForm(UserCreationForm):

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your first name'
        })
    )

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your last name'
        })
    )

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Choose a username'
        })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )

    phone = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your phone number'
        })
    )

    # =====================================================
    # INSTITUTION / COMPANY
    # =====================================================

    institution = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter institution / company name'
        }),
        label='Institution / Company'
    )

    # =====================================================
    # LOCATION
    # =====================================================

    location = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter city / location'
        }),
        label='Location / Place'
    )

    # =====================================================
    # ROLE
    # =====================================================

    role = forms.ChoiceField(
        choices=[
            ('CENTRAL_ADMIN', 'Central Administrator'),
            ('SUB_ADMIN', 'Sub Administrator'),
            ('RESEARCHER', 'Researcher'),
            ('TECHNICIAN', 'Technician'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'id_role'
        })
    )

    # =====================================================
    # SUPERVISOR
    # =====================================================

    supervisor = forms.ModelChoiceField(
        queryset=User.objects.filter(
            Q(is_superuser=True) |
            Q(lab_profile__role='SUB_ADMIN')
        ).distinct(),
        required=False,
        empty_label='Select Supervisor',
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'id_supervisor'
        })
    )

    # =====================================================
    # PASSWORD
    # =====================================================

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Create password'
        })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })
    )

    class Meta:

        model = User

        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'phone',
            'institution',
            'location',
            'role',
            'supervisor',
            'password1',
            'password2',
        )

    def clean(self):

        cleaned_data = super().clean()

        role = cleaned_data.get('role')
        supervisor = cleaned_data.get('supervisor')

        # =================================================
        # RESEARCHER / TECHNICIAN
        # =================================================

        if role in ['RESEARCHER', 'TECHNICIAN']:

            if supervisor is None:

                raise forms.ValidationError(
                    'Please select a supervisor for '
                    'Researcher or Technician.'
                )

        # =================================================
        # SUB ADMIN
        # =================================================

        if role == 'SUB_ADMIN':

            if supervisor is not None:

                raise forms.ValidationError(
                    'Sub Administrator should not have '
                    'a supervisor.'
                )

        # =================================================
        # CENTRAL ADMIN
        # =================================================

        if role == 'CENTRAL_ADMIN':

            if supervisor is not None:

                raise forms.ValidationError(
                    'Central Administrator should not have '
                    'a supervisor.'
                )

        return cleaned_data