from django.urls import reverse

from api.models import TaxBracket
from api.tests.base import APIBaseTest


class TaxBracketTests(APIBaseTest):
    list_url = reverse('taxbracket-list')

    def test_get_investments(self):
        tax_bracket = TaxBracket.objects.create(
            group='Federal',
            lower=0,
            upper=0,
            tax_rate=15,
            user=self.user,
        )

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]['group'], 'Federal')

    def test_create_tax_bracket(self):
        data = {
            'group': 'Federal',
            'lower': 50,
            'upper': 100,
            'tax_rate': 15.0,
            'user': self.user.id,
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, 201)


    def test_create_lower_above_upper(self):
        data = {
            'group': 'Federal',
            'lower': 100,
            'upper': 50,
            'tax_rate': 15.0,
            'user': self.user.id,
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, 400)
