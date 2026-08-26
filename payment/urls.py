from django.urls import path

from . import views


urlpatterns = [

    path(
        'checkout/<int:order_id>/',
        views.payment_checkout,
        name='payment_checkout'
    ),

    path(
        'success/<int:payment_id>/',
        views.payment_success,
        name='payment_success'
    ),

]