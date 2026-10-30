from datetime import datetime, timezone
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Booking, Menu
from .serializers import MenuSerializer


class MenuModelTest(TestCase):
    def test_str(self):
        item = Menu.objects.create(title='IceCream', price=Decimal('80.00'), inventory=100)
        self.assertEqual(str(item), 'IceCream : 80.00')


class BookingModelTest(TestCase):
    def test_str(self):
        booking = Booking.objects.create(
            name='Ann', no_of_guests=4,
            booking_date=datetime(2026, 11, 1, 19, 0, tzinfo=timezone.utc))
        self.assertEqual(str(booking), 'Ann')


class MenuViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        Menu.objects.create(title='IceCream', price=Decimal('80.00'), inventory=100)
        Menu.objects.create(title='Greek Salad', price=Decimal('12.50'), inventory=20)

    def test_getall(self):
        response = self.client.get('/api/menu/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, MenuSerializer(Menu.objects.all(), many=True).data)

    def test_get_single(self):
        item = Menu.objects.first()
        response = self.client.get(f'/api/menu/{item.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], item.title)

    def test_create_requires_auth(self):
        response = self.client.post('/api/menu/', {'title': 'Soup', 'price': '5.00', 'inventory': 3})
        self.assertEqual(response.status_code, 401)


class BookingApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('tester', password='pass12345!')
        self.payload = {'name': 'Ann', 'no_of_guests': 3, 'booking_date': '2026-11-01T19:00:00Z'}

    def test_booking_requires_auth_to_write(self):
        self.assertEqual(self.client.post('/api/bookings/', self.payload).status_code, 401)

    def test_booking_crud(self):
        self.client.force_authenticate(self.user)
        created = self.client.post('/api/bookings/', self.payload, format='json')
        self.assertEqual(created.status_code, 201)
        pk = created.data['id']
        self.assertEqual(self.client.get('/api/bookings/').status_code, 200)
        updated = self.client.put(f'/api/bookings/{pk}/', {**self.payload, 'no_of_guests': 5}, format='json')
        self.assertEqual(updated.data['no_of_guests'], 5)
        self.assertEqual(self.client.delete(f'/api/bookings/{pk}/').status_code, 204)
        self.assertEqual(Booking.objects.count(), 0)


class AuthTest(TestCase):
    def test_register_and_login(self):
        client = APIClient()
        reg = client.post('/auth/users/', {'username': 'newuser', 'password': 'Str0ngPass!42'})
        self.assertEqual(reg.status_code, 201)
        login = client.post('/auth/token/login/', {'username': 'newuser', 'password': 'Str0ngPass!42'})
        self.assertEqual(login.status_code, 200)
        self.assertIn('auth_token', login.data)

    def test_static_home_page(self):
        response = self.client.get('/')
        self.assertContains(response, 'Little Lemon')
