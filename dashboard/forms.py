from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


# ==========================================================
# SUB-ADMINISTRATOR FORM
# ==========================================================

class SubAdminForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Create password'
            }
        )
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Confirm password'
            }
        )
    )

    class Meta:

        model = User

        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
        ]

        widgets = {

            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'First name'
                }
            ),

            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Last name'
                }
            ),

            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Username'
                }
            ),

            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Email address'
                }
            ),
        }

    def clean_username(self):

        username = self.cleaned_data['username']

        if User.objects.filter(username=username).exists():

            raise forms.ValidationError(
                'This username already exists.'
            )

        return username

    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password:

            if password != confirm_password:

                raise forms.ValidationError(
                    'Passwords do not match.'
                )

        return cleaned_data

    def save(self, commit=True):

        user = super().save(commit=False)

        password = self.cleaned_data['password']

        user.set_password(password)

        user.is_staff = False
        user.is_superuser = False

        if commit:
            user.save()

        return user


# ==========================================================
# RESEARCHER / TECHNICIAN FORM
# ==========================================================

class TeamMemberForm(forms.ModelForm):

    ROLE_CHOICES = [
        ('RESEARCHER', 'Researcher'),
        ('TECHNICIAN', 'Technician'),
    ]

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.Select(
            attrs={
                'class': 'form-select'
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Create password'
            }
        )
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Confirm password'
            }
        )
    )

    class Meta:

        model = User

        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'role',
        ]

        widgets = {

            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'First name'
                }
            ),

            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Last name'
                }
            ),

            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Username'
                }
            ),

            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Email address'
                }
            ),
        }

    def clean_username(self):

        username = self.cleaned_data['username']

        if User.objects.filter(username=username).exists():

            raise forms.ValidationError(
                'This username already exists.'
            )

        return username

    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password:

            if password != confirm_password:

                raise forms.ValidationError(
                    'Passwords do not match.'
                )

        return cleaned_data

    def save(self, commit=True):

        user = super().save(commit=False)

        password = self.cleaned_data['password']

        user.set_password(password)

        # Researchers and technicians are normal users
        user.is_staff = False
        user.is_superuser = False

        if commit:
            user.save()

        return user