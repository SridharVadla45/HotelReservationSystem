from django.urls import path
from . import views

urlpatterns = [
    path('getListOfHotels', views.getListOfHotels, name='getListOfHotels'),
    path('reservationConfirmation', views.reservationConfirmation, name='reservationConfirmation'),
]
