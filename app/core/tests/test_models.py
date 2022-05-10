import uuid
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase

from core import models


def sample_user(name='Test', email='test@test.com', password='testpassword'):
    return get_user_model().objects.create(name, email, password)


class ModelTests(TestCase):

    def test_create_user_with_name_and_email_successful(self):
        name = 'Dawid'
        email = 'dawid@dawid11.com'
        password = 'zareba'
        user = get_user_model().objects.create_user(
            name=name,
            email=email,
            password=password
        )
        self.assertEqual(user.name, name)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        # Creating new user with normalized email
        email = 'test@test.com'
        user = get_user_model().objects.create_user(
            email=email,
            name='TestName',
            password='TestPassword'
        )
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        # Creating new user with no email raises error
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                name='TestName',
                email=None,
                password='TestPass'
            )

    def test_create_new_super_user(self):
        # Creating new superuser
        user = get_user_model().objects.create_superuser(
            name='TestName',
            email='test@test.com',
            password='TestPassword'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_genre_str(self):
        genre = models.Genre.objects.create(
            name='Fantasy'
        )
        self.assertEqual(str(genre), genre.name)

    def test_author_str(self):
        author = models.Author.objects.create(
            first_name='Andrzej',
            last_name='Sapkowski'
        )
        self.assertEqual(str(author), 'Andrzej Sapkowski')

    def test_publishing_house_str(self):
        publishing_house = models.PublishingHouse.objects.create(
            name='Helion'
        )
        self.assertEqual(str(publishing_house), 'Helion')

    @patch('uuid.uuid4')
    def test_book_str(self, mock_uuid):
        author = models.Author.objects.create(
            first_name='Andrzej',
            last_name='Sapkowski'
        )
        publishing_house = models.PublishingHouse.objects.create(
            name='Helion'
        )
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        genre = models.Genre.objects.create(
            name='Fantasy'
        )
        book = models.Book.objects.create(
            author=author,
            name='Wiedzmin Tom I',
            publishing_house=publishing_house,
            isbn=uuid,
            year_of_publish='2022-05-07',
            number_of_pages=300,
        )
        book.genre.set([genre])
        self.assertEqual(str(book), 'Wiedzmin Tom I')
