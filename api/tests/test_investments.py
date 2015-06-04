import json
from django.core.urlresolvers import reverse
from rest_framework.authtoken.models import Token
from rest_framework.renderers import JSONRenderer
from rest_framework.test import APITestCase
from api.models import Investment, User
from api.serializers import InvestmentSerializer


class InvestmentTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='one', email='one@exmaple.com', password='one')

        token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        self.url = reverse('investment-list')

    def test_get_investments(self):
        investment = Investment.objects.create(
            name='First', interest_rate=8.0,
            min_duration=0, balance=1000, user=self.user)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        #self.assertJSONEqual(json.dumps(json.loads(response.content)),
        #    JSONRenderer().render(InvestmentSerializer(data=investment)))
