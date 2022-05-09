from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Genre, Book
from book.serializers import GenreSerializer

GENRE_URL = reverse('book:genre-list')


class PublicGenreAPITests(TestCase):
    # Test the publicly available genre API

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        res = self.client.get(GENRE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateGenreAPITests(TestCase):
    # Test an authorized user genre API

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            name='TestName',
            email='genre@test.com',
            password='genrepass',
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_genres(self):
        # Test retrieving genres
        Genre.objects.create(name='Fantasy')
        Genre.objects.create(name='Education')

        res = self.client.get(GENRE_URL)

        genres = Genre.objects.all().order_by('-name')
        serializer = GenreSerializer(genres, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_genre_successful(self):
        # Test creating a new genre
        payload = {'name': 'Test genre'}
        self.client.post(GENRE_URL, payload)

        exists = Genre.objects.filter(
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_genre_invalid(self):
        # Test creating a new genre with invalid payload
        payload = {'name': ''}
        res = self.client.post(GENRE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_retrieve_genres_assigned_to_books(self):
    #     # Test filtering genres by those assigned to books
    #     genre1 = Genre.objects.create(name='Fantasy')
    #     genre2 = Genre.objects.create(name='Cooking')
    #
    #     book = Book.objects.create(
    #
    #     )