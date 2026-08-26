import uuid

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from external.models import ExternalOrder

from .forms import PaymentForm
from .models import Payment


@login_required
def payment_checkout(request, order_id):

    # Only external users can make payments
    if getattr(request.user, 'role', None) != 'EXTERNAL':

        messages.error(
            request,
            'Only external users can make payments.'
        )

        return redirect('home')


    # Get only the logged-in user's order
    order = get_object_or_404(
        ExternalOrder,
        id=order_id,
        user=request.user
    )


    # Don't allow payment again
    if order.status == 'PAID':

        messages.info(
            request,
            'This order has already been paid.'
        )

        return redirect('external_dashboard')


    if request.method == 'POST':

        form = PaymentForm(request.POST)

        if form.is_valid():

            payment = Payment.objects.create(

                user=request.user,

                order=order,

                amount=order.amount,

                payment_method=(
                    form.cleaned_data['payment_method']
                ),

                status='SUCCESS',

                transaction_id=(
                    'ICLMS-'
                    + uuid.uuid4().hex[:12].upper()
                )
            )


            # Mark order as paid
            order.status = 'PAID'
            order.save(
                update_fields=['status']
            )


            messages.success(
                request,
                'Payment completed successfully.'
            )


            return redirect(
                'payment_success',
                payment_id=payment.id
            )

    else:

        form = PaymentForm()


    return render(
        request,
        'payment_checkout.html',
        {
            'form': form,
            'order': order,
        }
    )


@login_required
def payment_success(request, payment_id):

    payment = get_object_or_404(
        Payment,
        id=payment_id,
        user=request.user
    )

    return render(
        request,
        'payment_success.html',
        {
            'payment': payment
        }
    )
