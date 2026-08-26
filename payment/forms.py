from django import forms


class PaymentForm(forms.Form):

    payment_method = forms.ChoiceField(
        choices=[
            ('UPI', 'UPI'),
            ('CARD', 'Credit / Debit Card'),
            ('NETBANKING', 'Net Banking'),
        ],
        widget=forms.Select(
            attrs={
                'class': 'form-select'
            }
        ),
        label='Payment Method'
    )