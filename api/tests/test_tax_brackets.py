from django.core.urlresolvers import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from api.models import TaxBracket, User


class TaxBracketTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='one', email='one@exmaple.com', password='one')

        token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        self.url = reverse('taxbracket-list')

    def test_get_investments(self):
        tax_bracket = TaxBracket.objects.create(
            lower=0, upper=0,
            tax_rate=15, user=self.user)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
