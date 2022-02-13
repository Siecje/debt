from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

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

    def setUp(self):
        super().setUp()
        # self.client is created before every test
        # So can't set this in setUpClass() (after setUpTestData() sets token_key)
        # Could create another client in setUpClass() to only set this once
        # but then you have to use self.api_client instead of self.client
        # Setting this before every test shouldn't be very slow right now
        # Maybe set it once if tests are slow
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_key)
