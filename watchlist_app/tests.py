from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User

from watchlist_app.api import serializers
from watchlist_app import models


class StreamTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='truongan',password='111111!!')
        self.token = Token.objects.get_or_create(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.stream = models.StreamPlatform.objects.create(name='netflix', about='lorem ipsum', web='http://www.netflix.com' )

    def test_streamCreate(self):
        data = {
            'name': 'netflix',
            'about': 'lorem ipsum',
            'web':'http://www.netflix.com'
        }
        response = self.client.post(reverse('streamplatformviewset-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_streamList(self):
        response = self.client.get(reverse('streamplatformviewset-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_streamInd(self):
        response = self.client.get(reverse('streamplatformviewset-detail', args=(self.stream.id)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class watchlistTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='truongan',password='111111!!')
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = models.StreamPlatform.objects.create(name='netflix', about='lorem ipsum', web='http://www.netflix.com' )
        self.watchlist = models.Watchlist.objects.create(title='ahihi', platform=self.stream, remarks='good', active=True)

    def test_watchlist_create(self):
        data = {
            'platform':self.stream,
            'title': 'lord of the ring',
            'remarks': 'good',
            'active': True
        }
        response = self.client.get(reverse('WatchlistListAPIView'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_watchlist_list(self):
        response = self.client.get(reverse('WatchlistListAPIView'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_watchlist_ind(self):
        response = self.client.get(reverse('WatchlistDetailAPIView', args=(self.watchlist.id)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.Watchlist.objects.get().title, 'lord of the ring')