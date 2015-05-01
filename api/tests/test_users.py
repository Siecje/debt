import json
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.renderers import JSONRenderer
from rest_framework.test import APIClient, APITestCase
from api.serializers import UserSerializer


class UserTests(APITestCase):
    def setUp(self):
        # Create superuser for tests
        self.admin = User.objects.create_superuser(
            username='Admin', email='admin@example.com', password='admin')
        # Get token
        url = reverse('auth-token')
        data = {
            'username': self.admin.username,
            'password': 'admin'
        }
        response = self.client.post(url, data, format='json')

        # Requests made with self.client will be as admin
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + response.data['token'])

        self.user_one = User.objects.create_user(
            username='one', email='one@exmaple.com', password='one')
        self.user_two = User.objects.create_user(
            username='two', email='two@exmaple.com', password='two')

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
        self.assertEqual(response.data, {'username': data['username']})

    def test_admin_can_view_all_user_list(self):
        """
        Ensure admins can view all users
        """
        response = self.client.get(reverse('user-list'))
        self.assertEqual(len(response.data), 3)
        self.assertJSONEqual(json.dumps(json.loads(response.content)),
            JSONRenderer().render([
                UserSerializer(self.admin).data,
                UserSerializer(self.user_one).data,
                UserSerializer(self.user_two).data]))

    def test_admin_can_view_user_detail(self):
        """
        Ensure admins can view a user's detail page
        """
        url = reverse('user-detail', kwargs={'pk': self.user_one.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(json.dumps(json.loads(response.content)),
                         JSONRenderer().render(UserSerializer(self.user_one).data))

    def test_admin_can_view_admin_detail(self):
        """
        Ensure admins can view an admin's detail page
        """
        admin_two = User.objects.create_superuser(
            username='admin_two', email='admin_two@example.com', password='admin')
        url = reverse('user-detail', kwargs={'pk': admin_two.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(json.dumps(json.loads(response.content)),
                 JSONRenderer().render(UserSerializer(admin_two).data))

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
        self.assertJSONEqual(json.dumps(json.loads(response.content)),
                 JSONRenderer().render([UserSerializer(self.user_one).data]))

    def test_user_can_view_own_detail(self):
        client = APIClient()
        token = Token.objects.get(user__username=self.user_one.username)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        url = reverse('user-detail', kwargs={'pk': self.user_one.pk})
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(json.dumps(json.loads(response.content)),
                 JSONRenderer().render(UserSerializer(self.user_one).data))

    def test_user_cannot_view_another_user_detail(self):
        client = APIClient()
        token = Token.objects.get(user__username=self.user_one.username)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        url = reverse('user-detail', kwargs={'pk': self.user_two.pk})
        response = client.get(url)
        self.assertEqual(response.status_code, 404)
