from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Author

from book.serializers import AuthorSerializer

AUTHOR_URL = reverse('book:author-list')


class PublicAuthorAPITests(TestCase):
    # Test public API
    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        # test login is required to the endpoint
        res = self.client.get(AUTHOR_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAuthorAPITests(TestCase):
    # Test the private author API
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            name='TestAuthor',
            email='author@test.com',
            password='testhaslo123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_author_list(self):
        # Test retrieving a list of authors
        Author.objects.create(first_name="Dawid", last_name="Zaręba")
        Author.objects.create(first_name="Antonio", last_name="Mele")

        res = self.client.get(AUTHOR_URL)

        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_author_successful(self):
        # Test create new author successful
        payload = {
            'first_name': 'Author',
            'last_name': 'Author'
        }
        self.client.post(AUTHOR_URL, payload)

        exists = Author.objects.filter(
            first_name=payload['first_name'],
            last_name=payload['last_name'],
        ).exists()

        self.assertTrue(exists)

    def test_create_author_invalid(self):
        payload = {
            'first_name': '',
            'last_name': 'Author'
        }
        res = self.client.post(AUTHOR_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
