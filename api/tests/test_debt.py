import json
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.renderers import JSONRenderer
from rest_framework.test import APIClient, APITestCase
from api.serializers import CreditCardSerializer
from api.models import CreditCard


class DebtTests(APITestCase):
    def test_get_debts(self):
        """
        Ensure we can create a new account object.
        """
        # Create a user with some debts
        user_one = User.objects.create_user(
            username='one', email='one@exmaple.com', password='one')

        credit_card = CreditCard(name='First', interest_rate='20',
                                 balance='1000', min_payment='100',
                                 min_payment_percent='15', annual_fee='100',
                                 user=user_one)
        print JSONRenderer().render([CreditCardSerializer(credit_card).data])
        credit_card.save()
        token = Token.objects.get(user__username=user_one.username)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        url = reverse('get-debts')
        response = self.client.get(url)
        # self.assertEqual(response.status_code, 200)
        # self.assertJSONEqual(json.dumps(json.loads(response.content)),
        #     JSONRenderer().render([CreditCardSerializer(credit_card).data]))
