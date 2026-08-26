from django import forms
from django.contrib.auth import get_user_model


User = get_user_model()


class ExternalRegistrationForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter password'
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

    external_type = forms.ChoiceField(
        choices=[
            ('TEACHER', 'Teacher'),
            ('STUDENT', 'Student'),
            ('OTHER', 'Other'),
        ],
        widget=forms.Select(
            attrs={
                'class': 'form-select'
            }
        ),
        label='User Type'
    )

    class Meta:

        model = User

        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'phone',
        ]

        widgets = {

            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter first name'
                }
            ),

            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter last name'
                }
            ),

            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Choose a username'
                }
            ),

            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter email address'
                }
            ),

            'phone': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter phone number'
                }
            ),
        }

        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'username': 'Username',
            'email': 'Email Address',
            'phone': 'Phone Number',
        }


    def clean_username(self):

        username = self.cleaned_data['username']

        if User.objects.filter(
            username=username
        ).exists():

            raise forms.ValidationError(
                'This username is already taken.'
            )

        return username


    def clean_email(self):

        email = self.cleaned_data['email']

        if User.objects.filter(
            email=email
        ).exists():

            raise forms.ValidationError(
                'An account with this email already exists.'
            )

        return email


    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get(
            'password'
        )

        confirm_password = cleaned_data.get(
            'confirm_password'
        )

        if (
            password
            and confirm_password
            and password != confirm_password
        ):

            raise forms.ValidationError(
                'Passwords do not match.'
            )

        return cleaned_data