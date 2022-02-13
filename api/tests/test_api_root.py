from django.urls import reverse

from api.tests.base import APIBaseTest


class APIRootTests(APIBaseTest):
    url = reverse('api-root')

    def test_api_root(self):
        expected_keys = {
            'credit-cards',
            'expenses',
            'incomes',
            'overdrafts',
            'types',
            'investments',
            'tax-brackets',
            'auth-token',
        }
        response = self.client.get(self.url)
        api_root_keys = set(response.json().keys())
        self.assertEqual(expected_keys, api_root_keys)
