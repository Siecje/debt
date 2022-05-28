import json

from django.urls import reverse

from api.models import DayOfWeek, Income, PayType
from api.serializers import IncomeSerializer
from api.tests.base import APIBaseTest


class IncomeTests(APIBaseTest):
    list_url = reverse('income-list')

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.income1 = Income.objects.create(
          name='Income1',
          pay_amount=100,
          pay_day=DayOfWeek.FRIDAY,
          pay_type=PayType.THIRTEEN_PAYS,
          user=cls.user,
        )

    def test_create_income_weekly(self):
        data = {
            'name': 'Weekly',
            'pay_amount': '100',
            'pay_day': DayOfWeek.labels[DayOfWeek.WEDNESDAY],
            'pay_type': PayType.labels[PayType.WEEKLY],
            'user': self.user.id,
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_create_income_biweekly(self):
        data = {
            'name': 'Biweekly',
            'pay_amount': '100',
            'pay_day': DayOfWeek.labels[DayOfWeek.WEDNESDAY],
            'pay_type': PayType.labels[PayType.BIWEEKLY],
            'user': self.user.id,
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_create_income_semi_monthly(self):
        data = {
            'name': 'Income',
            'pay_amount': '100',
            'pay_type': PayType.labels[PayType.SEMI_MONTHLY],
            'user': self.user.id,
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_create_income_monthly(self):
        data = {
            'name': 'Income',
            'pay_amount': '100',
            'pay_type': PayType.labels[PayType.MONTHLY],
            'user': self.user.id,
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_create_income_thirteen_pays(self):
        data = {
            'name': 'Income',
            'pay_amount': '100',
            'pay_day': DayOfWeek.labels[DayOfWeek.WEDNESDAY],
            'pay_type': PayType.labels[PayType.THIRTEEN_PAYS],
            'user': self.user.id,
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_income_list(self):
        response = self.client.get(self.list_url)
        expected = IncomeSerializer(self.income1).data
        self.assertEqual(
          json.loads(response.content)[0],
          expected
        )
        self.assertEqual(
          json.loads(response.content)[0]['pay_day'],
          'Friday',
        )
        # self.assertEqual(
        #   json.loads(response.content)[0]['pay_type'],
        #   'Weekly',
        # )
