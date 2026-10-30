Little Lemon - Back-end capstone project (Django + Django REST Framework + MySQL)

SETUP
1. python3 -m venv .venv && source .venv/bin/activate
2. pip install -r requirements.txt
3. Create a MySQL database:  CREATE DATABASE littlelemon;
4. Set credentials (defaults: user root, empty password, host 127.0.0.1):
   export DB_NAME=littlelemon DB_USER=root DB_PASSWORD=yourpassword
5. python manage.py migrate
6. python manage.py createsuperuser   (optional, for /admin/)
7. python manage.py runserver
8. Tests: python manage.py test

API PATHS TO TEST (base http://127.0.0.1:8000)
/                          static HTML home page
/api/menu/                 GET list, POST create (token required to write)
/api/menu/<id>/            GET, PUT, PATCH, DELETE a menu item
/api/bookings/             GET list, POST create (token required to write)
/api/bookings/<id>/        GET, PUT, PATCH, DELETE a booking
/auth/users/               POST {"username","password"} -> register a user
/auth/token/login/         POST {"username","password"} -> returns auth_token
/auth/token/logout/        POST (with token) -> log out

Authenticated requests need the header:  Authorization: Token <auth_token>
Example booking body:
{"name": "Ann", "no_of_guests": 3, "booking_date": "2026-11-01T19:00:00Z"}
Example menu body:
{"title": "Greek Salad", "price": "12.50", "inventory": 20}
