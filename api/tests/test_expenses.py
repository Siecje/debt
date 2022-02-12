import json

from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from api.models import Expense, Type, User


# When displaying type it should include the type's name
# when setting type you should only require the id

class ExpensesTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='one', email='one@exmaple.com', password='one')

        token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        self.type1 = Type.objects.create(name='First', user=self.user)
        self.type2 = Type.objects.create(name='Second', user=self.user)

    def test_create_expense_with_type(self):
        url = reverse('expense-list')
        data = {
            'name': 'Expense',
            'amount': '100',
            'frequency': '1',
            'type': self.type1.id,
            'user': self.user.id
        }
        response = self.client.post(url, data, format='json')
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
        self.assertEqual(json.loads(response.content)['type']['name'], 'First')

    def test_get_expense_list_has_type_names(self):
        expense = Expense.objects.create(
            name='Expense',
            amount=100,
            frequency=1,
            type=self.type1,
            user=self.user)
        url = reverse('expense-list')
        response = self.client.get(url)
        self.assertEqual(json.loads(response.content)[0]['type']['name'], 'First')
