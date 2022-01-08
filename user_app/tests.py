from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
# from rest_framework.test import APIClient

class SignInTestCase(APITestCase):

    def test_signin(self):
        data = {
            'username': 'truongan08',
            'email': 'truongan08@gmail.com',
            'password': '111111',
            'password2': '111111'
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    

class LoginTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='annhien', password='111111!!')

    def test_login(self):
        data = {
            'username': 'annhien',
            'password': '111111!!'
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_logout(self):
    #     self.token = Token.objects.get(user__username='annhien')
    #     self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    #     response = self.client.post(reverse('logout'))
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)