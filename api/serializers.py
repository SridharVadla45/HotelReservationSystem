from rest_framework import serializers
from .models import Hotel, Reservation, Guest

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ['name']

class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ['guest_name', 'gender']

class ReservationSerializer(serializers.ModelSerializer):
    guests_list = GuestSerializer(many=True)
    hotel_name = serializers.CharField(write_only=True)
    
    class Meta:
        model = Reservation
        fields = ['hotel_name', 'checkin', 'checkout', 'guests_list', 'confirmation_number']
        read_only_fields = ['confirmation_number']

    def validate(self, data):
        checkin = data.get('checkin')
        checkout = data.get('checkout')

        if checkin and checkout and checkout <= checkin:
            raise serializers.ValidationError({"checkout": "Check-out date must be after check-in date."})

        return data

    def create(self, validated_data):
        guests_data = validated_data.pop('guests_list', [])
        hotel_name_input = validated_data.pop('hotel_name')
        
        hotel, _ = Hotel.objects.get_or_create(name=hotel_name_input)
        
        reservation = Reservation.objects.create(hotel=hotel, **validated_data)
        
        for guest_data in guests_data:
            Guest.objects.create(reservation=reservation, **guest_data)
            
        return reservation
