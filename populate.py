import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_reservation_system.settings')
django.setup()

from api.models import Hotel

def populate():
    hotels = [
        "The Ritz-Carlton",
        "Marriott Marquis",
        "Hilton Downtown",
        "Holiday Inn Express",
        "Four Seasons Resort",
        "Grand Hyatt"
    ]
    
    for name in hotels:
        Hotel.objects.get_or_create(name=name)
    
    print("Successfully populated mock hotels.")

if __name__ == '__main__':
    populate()
