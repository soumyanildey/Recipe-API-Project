"""
Tests for User API
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicUserAPITest(TestCase):
    '''Test the public features of the User API'''

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        '''Test creating a user is successful.'''
        payload = {
            'email': 'test@example.com',
            'password': 'testpassword123',
            'name': 'Test Name',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_if_email_exists_error(self):
        """Test Error returned if user with email exists"""
        payload = {
            'email': 'test@example.com',
            'password': 'test123',
            'name': 'Test Name'
        }

        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Password less than 5 chars"""
        payload = {
            'email': 'test@example.com',
            'password': 'pw',
            'name': 'Test Name',
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_auth_api(self):
        '''Creates token for Auth API for Valid Credentials'''
        user = {
            'name': 'Test Name',
            'email': 'test@example.com',
            'password': 'pass123'
        }
        create_user(**user)
        payload = {
            'email': user['email'],
            'password': user['password'],
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_for_bad_credentials(self):
        '''Check for error in Bad Credentials'''

        create_user(email='test@example.com', password='goodpass')
        payload = {'email': 'test@example.com', 'password': 'badpass'}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_for_blank_password(self):
        '''Check for blank password'''

        payload = {'email': 'test@example.com', 'password': ''}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_for_unauthorized_access(self):
        '''Check for public unauthorized entry ot the API'''
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserAPITest(TestCase):
    """Test for Authorized Access"""

    def setUp(self):
        self.user = create_user({
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        })

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_for_retrieve_profile(self):
        '''Test for Profile Retrieval'''
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'email': self.user.email,
            'name': self.user.name,
        })

    def test_post_not_allowed(self):
        '''POST not allowed for GET API'''

        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        '''Check for Updating User Profile'''

        payload = {
            'name': 'Toast Name',
            'password': 'newpass123',
        }

        res = self.client.patch(ME_URL, payload)

        self.assertEqual(res.status, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
