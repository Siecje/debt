import json
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.renderers import JSONRenderer
from rest_framework.test import APIClient, APITestCase
from api.serializers import CreditCardSerializer, OverdraftSerializer
from api.models import CreditCard, Overdraft


class DebtTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='one', email='one@exmaple.com', password='one')

        self.credit_card = CreditCard(name='First', interest_rate='20',
                                      balance='1000', min_payment='100',
                                      min_payment_percent='15', annual_fee='100',
                                      user=self.user)
        self.credit_card.save()

        token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_get_debts(self):
        url = reverse('get-debts')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(json.dumps(json.loads(response.content)),
            JSONRenderer().render([CreditCardSerializer(self.credit_card).data]))

    def test_get_debts_with_overdraft_and_credit_card(self):
        overdraft = Overdraft(name='Brick & Mortar', balance=1000,
                              monthly_fee=4, interest_rate=0.21, user=self.user)
        url = reverse('get-debts')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(json.dumps(json.loads(response.content)),
                  JSONRenderer().render([OverdraftSerializer(overdraft).data,
                  CreditCardSerializer(self.credit_card).data]))
