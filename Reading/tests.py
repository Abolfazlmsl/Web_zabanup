from django.test import TestCase
from django.contrib.auth.models import User as us
from django.contrib.auth import authenticate, login

# Create your tests here.


class User(TestCase):
    def setUp(self):
        us.objects.create_user(email='mr.amirhossein1836@gmail.com', first_name='amirhossein', password='Amir1376', last_name='asadi', username='amirhossein')
        us.objects.create_user(email='mr.amirhossein@gmail.com', first_name='amirhossein', password='Amir1376', last_name='asadi', username='am13ir76')

    def test_login(self):
        response = self.client.post('/login/', {'username': 'amirhossein', 'password': 'Amir1376'})
        self.assertEqual(response.status_code, 302)

    def test_signup(self):
        response = self.client.post('/signup/', {'username': 'mediasoft',
                                                 'password': 'Amir1376',
                                                 're_password': 'Amir1376',
                                                 'email': 'mediasoft@gmail.com',
                                                 'first_name': 'amirhossein',
                                                 'last_name': 'asadi',
                                                 'phone_number': '09331532578',
                                                 'address': 'Tehran',
                                                 }
                                    )
        self.assertEqual(response.status_code, 302)

    def test_changePassword(self):
        self.client.login(username='am13ir76', password='Amir1376')
        response = self.client.post('/change_password/', {'user': 'am13ir76', 'newpass': 'amir1376'})
        self.assertEqual(response.status_code, 302)
