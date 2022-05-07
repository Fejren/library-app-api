from django.contrib.auth import get_user_model
from django.test import TestCase

def sample_user(name='Test', email='test@test.com', password='testpassword'):
    return get_user_model().objects.create(name, email, password)


class ModelTests(TestCase):

    def test_create_user_with_name_and_email_successful(self):
        name = 'Dawid'
        email = 'dawid@dawid.com'
        password = 'zareba'
        user = get_user_model().objects.create_user(
            name=name,
            email=email,
            password=password
        )
        self.assertEqual(user.name, name)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
    
    
