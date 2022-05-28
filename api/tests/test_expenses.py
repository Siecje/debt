import json

from django.urls import reverse
from rest_framework.authtoken.models import Token

from api.models import Expense, Type
from api.tests.base import APIBaseTest


# When displaying type it should include the type's name
# when setting type you should only require the id

class ExpensesTests(APIBaseTest):
    list_url = reverse('expense-list')
    
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.type1 = Type.objects.create(name='First', user=cls.user)
        cls.type2 = Type.objects.create(name='Second', user=cls.user)

    def test_create_expense_with_type(self):
        data = {
            'name': 'Expense',
            'amount': '100',
            'frequency': '1',
            'type': self.type1.id,
            'user': self.user.id
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_edit_expense_with_type(self):
        expense = Expense.objects.create(
            name='Expense',
            amount=100,
            frequency=1,
            type=self.type1,
            user=self.user)
        url = reverse('expense-detail', kwargs={'pk': expense.id})
        data = {
            'name': 'Different',
            'amount': '100',
            'frequency': '1',
            'type': self.type1.id,
            'user': self.user.id
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_change_expense_type(self):
        expense = Expense.objects.create(
            name='Expense',
            amount=100,
            frequency=1,
            type=self.type1,
            user=self.user)
        url = reverse('expense-detail', kwargs={'pk': expense.id})
        data = {
            'type': self.type2.id
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_get_expense_has_type_name(self):
        expense = Expense.objects.create(
            name='Expense',
            amount=100,
            frequency=1,
            type=self.type1,
            user=self.user)
        url = reverse('expense-detail', kwargs={'pk': expense.id})
        response = self.client.get(url)
        type_from_response = json.loads(response.content)['type']
        self.assertEqual(type_from_response['name'], self.type1.name)
        self.assertEqual(type_from_response['url'], self.type1.get_absolute_url())
        self.assertEqual(type_from_response['id'], str(self.type1.id))

    def test_get_expense_list_has_type_names(self):
        expense = Expense.objects.create(
            name='Expense',
            amount=100,
            frequency=1,
            type=self.type1,
            user=self.user,
        )
        response = self.client.get(self.list_url)
        self.assertEqual(json.loads(response.content)[0]['type']['name'], 'First')
