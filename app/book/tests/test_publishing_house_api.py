from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from core.models import PublishingHouse
from book.serializers import PublishingHouseSerializer

PHOUSE_URL = reverse('book:publishinghouse-list')


class PublicPublishingHouseAPITests(TestCase):
    # Test public API
    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        # test login is required to the endpoint
        res = self.client.get(PHOUSE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivatePublishingHouseAPITests(TestCase):
    # Test the private phouse API
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            name='TestName',
            email='phouse@test.com',
            password='testhaslo123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_phouse_list(self):
        # Test retrieving a list of phouses
        PublishingHouse.objects.create(name="TestName")
        PublishingHouse.objects.create(name="TestName2")

        res = self.client.get(PHOUSE_URL)

        phouses = PublishingHouse.objects.all()
        serializer = PublishingHouseSerializer(phouses, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_phouse_successful(self):
        # Test create new phouse successful
        payload = {
            'name': 'TestName',
        }
        self.client.post(PHOUSE_URL, payload)

        exists = PublishingHouse.objects.filter(
            name=payload['name'],
        ).exists()

        self.assertTrue(exists)

    def test_create_phouse_invalid(self):
        # Test create new phouse invalid
        payload = {
            'name': '',
        }
        res = self.client.post(PHOUSE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
