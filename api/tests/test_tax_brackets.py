from django.urls import reverse

from api.models import TaxBracket
from api.tests.base import APIBaseTest


class TaxBracketTests(APIBaseTest):
    url = reverse('taxbracket-list')

    def test_get_investments(self):
        tax_bracket = TaxBracket.objects.create(
            lower=0,
            upper=0,
            tax_rate=15,
            user=self.user,
        )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
