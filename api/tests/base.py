from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from api.models import User


class APIBaseTest(APITestCase):
    token_key = None

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        # Data required for any (all) test
        cls.user = User.objects.create_user(
            username='one',
            email='one@exmaple.com',
            password='one',
        )

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
