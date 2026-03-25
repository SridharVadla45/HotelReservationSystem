# Hotel Reservation System API

This project provides a REST API for a Hotel Reservation System developed using Django and Django Rest Framework (DRF) as per the assignment specifications.

## Requirements Covered
- RESTful HTTP Methods (`GET`, `POST`)
- Proper SDLC flow using Git commits
- Data storage via SQLite database (mock hotels, dynamically generated reservations/guests)
- Nested JSON payloads (Gues list inside Reservation)
- Validation (Ensure `checkout` is after `checkin`)
- Clear README for Marker evaluation

## Setup Instructions

1. **Prerequisites**: Ensure you have Python 3 and Git installed.
   ```bash
   # Clone the repository (if applicable)
   # git clone <repo_url>
   # cd DjangoAssignment
   ```

2. **Set up the virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the dependencies**:
   ```bash
   pip install django djangorestframework
   ```

4. **Run migrations to set up the SQLite DB**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Populate Database with Mock Hotel Data** (Optional, already included if `db.sqlite3` is copied):
   ```bash
   python populate.py
   ```

6. **Run the local development server**:
   ```bash
   python manage.py runserver
   ```
   The API will now be running at `http://localhost:8000/`.

---

## API Documentation

### 1. `getListOfHotels`

- **HTTP Method**: `GET`
- **URL**: `http://localhost:8000/getListOfHotels`
- **Description**: Returns a list of hotels from the mock dataset. You can pass `checkin` and `checkout` dates to dynamically filter the list, ensuring hotels already booked across those dates do not appear.
- **Query Parameters** (Optional):
  - `checkin` (YYYY-MM-DD): The check-in date.
  - `checkout` (YYYY-MM-DD): The check-out date.

**Example Request:**
```bash
curl -X GET "http://localhost:8000/getListOfHotels?checkin=2026-05-01&checkout=2026-05-05"
```

**Example Response:**
```json
[
    {
        "name": "The Ritz-Carlton"
    },
    {
        "name": "Marriott Marquis"
    },
    {
        "name": "Hilton Downtown"
    }
]
```

### 2. `reservationConfirmation`

- **HTTP Method**: `POST`
- **URL**: `http://localhost:8000/reservationConfirmation`
- **Description**: Creates a new hotel reservation associating the specified guests to it. If the hotel does not exist yet, this endpoint will dynamically create it. Returns a unique confirmation number.
- **Headers**:
  - `Content-Type: application/json`

**Example Request payload:**
```json
{
    "hotel_name": "The Ritz-Carlton",
    "checkin": "2026-05-01",
    "checkout": "2026-05-05",
    "guests_list": [
        {
            "guest_name": "John Doe",
            "gender": "Male"
        },
        {
            "guest_name": "Jane Doe",
            "gender": "Female"
        }
    ]
}
```

**Example CURL:**
```bash
curl -X POST http://localhost:8000/reservationConfirmation \
-H "Content-Type: application/json" \
-d '{
    "hotel_name": "The Ritz-Carlton",
    "checkin": "2026-05-01",
    "checkout": "2026-05-05",
    "guests_list": [
        { "guest_name": "John Doe", "gender": "Male" },
        { "guest_name": "Jane Doe", "gender": "Female" }
    ]
}'
```

**Example Response (201 Created):**
```json
{
    "confirmation_number": "4BCAF89D21"
}
```

**Example Validation Error Response (400 Bad Request):**
```json
{
    "checkout": [
        "Check-out date must be after check-in date."
    ]
}
```

## Testing Strategy
Use [Postman](https://www.postman.com/) or another HTTP client. Create a `POST` request to `http://localhost:8000/reservationConfirmation` using raw JSON from the example payload to see the database create validation errors and confirmation numbers.
Check the hotel availability by modifying the parameters in the `GET` endpoint `http://localhost:8000/getListOfHotels`.
