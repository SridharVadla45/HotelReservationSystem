from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from .models import Hotel, Reservation
from .serializers import HotelSerializer, ReservationSerializer

@extend_schema(
    parameters=[
        OpenApiParameter(name='checkin', type=OpenApiTypes.DATE, location=OpenApiParameter.QUERY, description='Check-in date (YYYY-MM-DD)'),
        OpenApiParameter(name='checkout', type=OpenApiTypes.DATE, location=OpenApiParameter.QUERY, description='Check-out date (YYYY-MM-DD)')
    ],
    responses=HotelSerializer(many=True),
    description="Returns the list of hotels available in the system. Filters hotels based on provided check-in and check-out dates via query params."
)
@api_view(['GET'])
def getListOfHotels(request):
    """
    Returns the list of hotels available in the system.
    Filters hotels based on provided check-in and check-out dates via query params.
    """
    checkin_date = request.query_params.get('checkin')
    checkout_date = request.query_params.get('checkout')

    hotels = Hotel.objects.all()

    if checkin_date and checkout_date:
        # Exclude hotels that are fully booked (For simplicity, assume any overlapping reservation blocks the entire hotel for now,
        # or we just exclude hotels that have ANY reservations during that time - the requirement just says "change based on check-in/out dates")
        # To be realistic without a room concept: just an example of list changing based on dates. Let's exclude hotels that are booked for those exact dates.
        overlapping_reservations = Reservation.objects.filter(
            hotel__in=hotels,
            checkin__lt=checkout_date,
            checkout__gt=checkin_date
        )
        booked_hotel_ids = overlapping_reservations.values_list('hotel_id', flat=True)
        hotels = hotels.exclude(id__in=booked_hotel_ids)

    serializer = HotelSerializer(hotels, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@extend_schema(
    request=ReservationSerializer,
    responses={
        201: OpenApiTypes.OBJECT,
        400: OpenApiTypes.OBJECT
    },
    description="Creates a hotel reservation and returns a confirmation number."
)
@api_view(['POST'])
def reservationConfirmation(request):
    """
    Creates a hotel reservation and returns a confirmation number.
    Expects hotel_name, checkin, checkout, and guests_list.
    """
    serializer = ReservationSerializer(data=request.data)
    
    if serializer.is_valid():
        reservation = serializer.save()
        response_data = {
            "confirmation_number": reservation.confirmation_number
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
