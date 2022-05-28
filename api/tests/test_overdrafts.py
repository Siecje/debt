import json

from django.urls import reverse

from api.models import Overdraft
from api.serializers import OverdraftSerializer
from api.tests.base import APIBaseTest


class OverdraftTests(APIBaseTest):
    list_url = reverse('overdraft-list')

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.overdraft = Overdraft.objects.create(
          name='Overdraft',
          balance=1000,
          interest_rate=21.00,
          monthly_fee=500,
          user=cls.user,
        )

    def test_create_overdraft(self):
        data = {
            'name': 'Overdraft',
            'interest_rate': '19.99',
            'balance': '2000',
            'monthly_fee': '300',
            'user': self.user.id
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_get_list(self):
        response = self.client.get(self.list_url)
        expected = OverdraftSerializer(self.overdraft).data
        overdraft_from_response = json.loads(response.content)[0]
        self.assertEqual(
          overdraft_from_response,
          expected
        )
        self.assertEqual(
            overdraft_from_response['url'],
            self.overdraft.get_absolute_url()
        )

    def test_timeline_monthly_payment_less_than_min_payment(self):
        timeline = self.overdraft.timeline(100)
        self.assertEqual(timeline['num_months'], -1)
