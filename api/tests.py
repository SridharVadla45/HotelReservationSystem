from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Hotel, Reservation, Guest

class ReservationTests(APITestCase):

    def setUp(self):
        self.hotel = Hotel.objects.create(name="The Ritz-Carlton")

    def test_get_list_of_hotels(self):
        url = reverse('getListOfHotels')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # We expect a list containing our setup hotel
        self.assertEqual(len(response.data), 1)

    def test_create_reservation(self):
        url = reverse('reservationConfirmation')
        data = {
            "hotel_name": "The Ritz-Carlton",
            "checkin": "2026-05-01",
            "checkout": "2026-05-05",
            "guests_list": [
                { "guest_name": "John Doe", "gender": "Male" },
                { "guest_name": "Jane Doe", "gender": "Female" }
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('confirmation_number', response.data)
        
        # Verify db logic
        self.assertEqual(Reservation.objects.count(), 1)
        self.assertEqual(Guest.objects.count(), 2)
        reservation = Reservation.objects.first()
        self.assertEqual(reservation.guests_list.count(), 2)

    def test_validation_checkout_before_checkin(self):
        url = reverse('reservationConfirmation')
        data = {
            "hotel_name": "The Ritz-Carlton",
            "checkin": "2026-05-05",
            "checkout": "2026-05-01",
            "guests_list": [
                { "guest_name": "John Doe", "gender": "Male" }
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('checkout', response.data)

    def test_hotel_filter_based_on_reservation(self):
        # Create a booking
        url_post = reverse('reservationConfirmation')
        data = {
            "hotel_name": "The Ritz-Carlton",
            "checkin": "2026-05-01",
            "checkout": "2026-05-05",
            "guests_list": [{"guest_name": "John Doe", "gender": "Male"}]
        }
        self.client.post(url_post, data, format='json')

        # Try to look for hotels during this exact timeframe
        url_get = reverse('getListOfHotels')
        response = self.client.get(url_get, {'checkin': '2026-05-02', 'checkout': '2026-05-04'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # The hotel should be excluded because it has a reservation in this overlapping time
        self.assertEqual(len(response.data), 0)
