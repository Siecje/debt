from django.urls import reverse

from api.models import Investment
from api.serializers import InvestmentSerializer
from api.tests.base import APIBaseTest


class InvestmentTests(APIBaseTest):
    url = reverse('investment-list')

    def test_get_investments(self):
        investment = Investment.objects.create(
            name='First',
            interest_rate=8.0,
            min_duration=0,
            balance=1000,
            user=self.user,
        )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            [InvestmentSerializer(investment).data],
        )
