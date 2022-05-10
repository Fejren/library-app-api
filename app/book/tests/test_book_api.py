import tempfile
import os
from PIL import Image
from django.contrib.auth import get_user_model

from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Book, Author, Genre, PublishingHouse, BookInstance
from book.serializers import BookSerializer, BookDetailSerializer, \
    BookInstanceSerializer

BOOK_URL = reverse('book:book-list')
BOOK_INSTANCE_URL = reverse('book:bookinstance-list')

def image_upload_url(book_id):
    # Return URL for book img upload
    return reverse('book:book-upload-image', args=[book_id])


def detail_url(book_id):
    # Return book detail url
    return reverse('book:book-detail', args=[book_id])


def sample_genre(name='Sample Genre'):
    # Create sample genre
    return Genre.objects.create(name=name)


def sample_author(first_name='Andrzej', last_name='Sapkowski'):
    # Create sample author
    return Author.objects.create(first_name=first_name, last_name=last_name)


def sample_publishing_house(name='SuperNowa'):
    # Create sample publishing house
    return PublishingHouse.objects.create(name=name)


def sample_book(**params):
    # Create sample book
    defaults = {
        'name': 'Wiedzmin',
        'number_of_pages': 300,
        'year_of_publish': '2000-11-11',
        'summary': '*jakies streszczenie*',
        'isbn': '978-83-7578-063-5',
    }
    defaults.update(**params)

    return Book.objects.create(**defaults)


def complete_book_obj():
    publishing_house = sample_publishing_house()
    author = sample_author()
    genre = sample_genre()

    book = sample_book(
        author=author,
        publishing_house=publishing_house
    )
    book.genre.set([genre])

    return book


class PrivateBookAPITest(TestCase):
    # Test auth book API access

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            name='TestName',
            email='book@test.com',
            password='bookpass',
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_book(self):
        # Test retrieving a list of recipes
        complete_book_obj()
        res = self.client.get(BOOK_URL)

        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


class PrivateBookInstanceAPITest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            name='TestName',
            email='book@test.com',
            password='bookpass',
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_book_instance(self):
        book = complete_book_obj()
        user = get_user_model().objects.create_user(
            name='User',
            email='user@user.com',
            password='userpass'
        )
        book_instance = BookInstance.objects.create(
            book=book,
            status='a',
        )
        book_instance.user.set([user])
        res = self.client.get(BOOK_INSTANCE_URL)
        book_instances = BookInstance.objects.all()
        serializer = BookInstanceSerializer(book_instances, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
