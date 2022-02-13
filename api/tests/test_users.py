import json

from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from api.models import User
from api.serializers import UserSerializer


class UserTests(APITestCase):
    token_key = None

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        # Create superuser for tests
        cls.admin = User.objects.create_superuser(
            username='Admin',
            email='admin@example.com',
            password='admin',
        )
        # Get token
        url = reverse('auth-token')
        data = {
            'username': cls.admin.username,
            'password': 'admin'
        }
        client = APIClient()
        response = client.post(url, data, format='json')
        cls.token_key = response.data['token']

        cls.user_one = User.objects.create_user(
            username='one',
            email='one@exmaple.com',
            password='one',
        )
        cls.user_two = User.objects.create_user(
            username='two',
            email='two@exmaple.com',
            password='two',
        )

    def setUp(self):
        # Requests made with self.client will be as admin
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_key)

    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('user-list')
        data = {
            'username': 'Unique',
            'email': 'unique@example.com',
            'password': 'unique'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username='Unique')
        self.assertEqual(response.data, UserSerializer(user).data)

    def test_admin_can_view_all_user_list(self):
        """
        Ensure admins can view all users
        """
        response = self.client.get(reverse('user-list'))
        self.assertEqual(len(response.data), 3)
        self.assertJSONEqual(
            response.content,
            [
                UserSerializer(self.admin).data,
                UserSerializer(self.user_one).data,
                UserSerializer(self.user_two).data
            ],
        )

    def test_admin_can_view_user_detail(self):
        """
        Ensure admins can view a user's detail page
        """
        url = reverse('user-detail', kwargs={'pk': self.user_one.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            UserSerializer(self.user_one).data,
        )

    def test_admin_can_view_admin_detail(self):
        """
        Ensure admins can view an admin's detail page
        """
        admin_two = User.objects.create_superuser(
            username='admin_two',
            email='admin_two@example.com',
            password='admin',
        )
        url = reverse('user-detail', kwargs={'pk': admin_two.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            UserSerializer(admin_two).data,
        )

    def test_anon_cannot_view_user_list(self):
        """
        Anonymous user should see empty list
        """
        client = APIClient()
        response = client.get(reverse('user-list'))
        self.assertEqual(len(response.data), 0)

    def test_user_cannot_view_user_list(self):
        """
        Ensure user can only see themself in user list
        """
        client = APIClient()
        token = Token.objects.get(user__username=self.user_one.username)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        url = reverse('user-list')
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertJSONEqual(
            response.content,
            [UserSerializer(self.user_one).data],
        )

    def test_user_can_view_own_detail(self):
        client = APIClient()
        token = Token.objects.get(user__username=self.user_one.username)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        url = reverse('user-detail', kwargs={'pk': self.user_one.pk})
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            UserSerializer(self.user_one).data,
        )

    def test_user_cannot_view_another_user_detail(self):
        client = APIClient()
        token = Token.objects.get(user__username=self.user_one.username)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        url = reverse('user-detail', kwargs={'pk': self.user_two.pk})
        response = client.get(url)
        self.assertEqual(response.status_code, 404)
