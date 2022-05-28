import json

from django.urls import reverse

from api.models import CreditCard
from api.serializers import CreditCardSerializer
from api.tests.base import APIBaseTest


class CreditCardTests(APIBaseTest):
    list_url = reverse('creditcard-list')

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.credit_card = CreditCard.objects.create(
          name='CreditCard',
          interest_rate=19.99,
          balance=1000,
          min_payment=10,
          min_payment_percent=10,
          annual_fee=0,
          user=cls.user,
        )

    def test_create_credit_card(self):
        data = {
            'name': 'CreditCard',
            'interest_rate': '19.99',
            'balance': '1000',
            'min_payment': '10',
            'min_payment_percent': '10',
            'annual_fee': '50',
            'user': self.user.id
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_get_list(self):
        response = self.client.get(self.list_url)
        expected = CreditCardSerializer(self.credit_card).data
        credit_card_from_response = json.loads(response.content)[0]
        self.assertEqual(
          credit_card_from_response,
          expected
        )
        self.assertEqual(
            credit_card_from_response['url'],
            self.credit_card.get_absolute_url()
        )

    def test_timeline_monthly_payment_less_than_min_payment(self):
        timeline = self.credit_card.timeline(self.credit_card.min_payment - 1)
        self.assertEqual(timeline['num_months'], -1)
