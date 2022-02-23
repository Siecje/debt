from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from api.models import User


class APIBaseTest(APITestCase):
    token_key = None

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        # Data required for any (all) test
        get_user_model().objects.create_user(
            username='one',
            email='one@exmaple.com',
            password='one',
        )
        # So user has additional methods
        cls.user = User.objects.get(username='one')

        token = Token.objects.get(user__username=cls.user.username)
        cls.token_key = token.key

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.api_client = APIClient()
        cls.api_client.credentials(HTTP_AUTHORIZATION='Token ' + cls.token_key)

    def setUp(self):
        super().setUp()
        # self.client is created before every test
        # This allows the tests to use self.client
        self.client = self.api_client
