from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserAPITests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_create_valid_user_success(self):
        # Test creating user with valid payload
        payload = {
            'email': 'isvalid@test.com',
            'password': 'isvaliduser',
            'name': 'TestName'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        # Test creating user that already exists
        payload = {
            'email': 'isvalid@test.com',
            'name': 'TestName',
            'password': 'isvaliduser',
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        # Password must be more than 6 characters
        payload = {
            'email': 'isvalid@test.com',
            'name': 'TestName',
            'password': '1234',
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        # Test that a token is created for the user
        payload = {
            'email': 'isvalid@test.com',
            'name': 'TestName',
            'password': 'isvaliduser',
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        # Test token is not created if invalid credentials
        create_user(email='token@test.com', name='TestName', password='testpass1')
        payload = {
            'email': 'token@test.com',
            'name': 'TestName',
            'password': 'wrongpassword',
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        # Test that token isn't created if user doesn't exist
        payload = {
            'email': 'isvalid@test.com',
            'name': 'TestName',
            'password': 'isvaliduser',
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_fields(self):
        payload = {
            'email': 'isvalid@test.com',
            'name': 'TestName',
            'password': '',
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        # Test that auth is required for users
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserAPITests(TestCase):
    # Test API request that require auth
    def setUp(self):
        self.user = create_user(
            email='test@test.com',
            password='test12345',
            name='TestName'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_post_me_not_allowed(self):
        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # Old test
    # def test_update_me_not_allowed(self):
    #     payload = {'name': 'NewTestName', 'password': 'gigapssswrd123'}
    #     res = self.client.patch(ME_URL, payload)
    #
    #     self.user.refresh_from_db()
    #     self.assertNotEqual(self.user.name, payload['name'])
    #     self.assertFalse(self.user.check_password(payload['password']))
    #     self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    #
    def test_update_me_allowed(self):
        payload = {'name': 'NewTestName', 'password': 'gigapssswrd123'}
        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_retrieve_profile_success(self):
        # Test retrieving profile for logged in used
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email,
        })
