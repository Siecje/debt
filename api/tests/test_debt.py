import json

from django.urls import reverse

from api.models import CreditCard, Income, Overdraft, PayType
from api.tests.base import APIBaseTest


class DebtTests(APIBaseTest):
    url = reverse('get-debts')

    def test_get_debts(self):
        credit_card = CreditCard.objects.create(
            name='First',
            interest_rate=20.0,
            balance=1000,
            min_payment=10,
            min_payment_percent=15.0,
            annual_fee=100,
            user=self.user,
        )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            [credit_card.to_JSON()],
        )

    def test_credit_cards_sorted_by_interest_rate(self):
        balance1 = 1_000
        card1 = CreditCard.objects.create(
            name='One',
            interest_rate=20.0,
            balance=balance1,
            min_payment=10,
            min_payment_percent=10.0,
            annual_fee=100,
            user=self.user,
        )
        balance2 = 2_000
        card2 = CreditCard.objects.create(
            name='Two',
            interest_rate=20.1,
            balance=balance2,
            min_payment=10,
            min_payment_percent=10.0,
            annual_fee=100,
            user=self.user,
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            [card2.to_JSON(), card1.to_JSON()],
        )
        self.assertEqual(self.user.get_total_debt(), balance1 + balance2)

    def test_debts_sorted_by_fee(self):
        """
        Montly/Annual costs should be considered
        """
        card = CreditCard.objects.create(
            name='One',
            interest_rate=20.0,
            balance=1000,
            min_payment=10,
            min_payment_percent=10.0,
            annual_fee=100,
            user=self.user,
        )
        overdraft = Overdraft.objects.create(
            name='Over',
            interest_rate=20.0,
            balance=1000,
            monthly_fee=9,
            user=self.user,
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            [overdraft.to_JSON(), card.to_JSON()],
        )

    def test_debts_sorted_properly(self):
        """
        Interest rate, fees, should be taken into consideration
        """
        # An example where the higher interest rate
        # will not cost more than the annual fee
        card1 = CreditCard.objects.create(
            name='One',
            interest_rate=20.0,
            balance=1000,
            min_payment=10,
            min_payment_percent=10.0,
            annual_fee=111,
            user=self.user,
        )
        card2 = CreditCard.objects.create(
            name='Two',
            interest_rate=21.0,
            balance=1000,
            min_payment=10,
            min_payment_percent=10.0,
            annual_fee=100,
            user=self.user,
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            [card1.to_JSON(), card2.to_JSON()],
        )

    def test_debts_cc_and_overdraft_sorted(self):
        card = CreditCard.objects.create(
            name='One',
            interest_rate=20.0,
            balance=1000,
            min_payment=10,
            min_payment_percent=10.0,
            annual_fee=100,
            user=self.user,
        )
        overdraft = Overdraft.objects.create(
            name='Over',
            interest_rate=21.0,
            balance=1000,
            monthly_fee=5,
            user=self.user,
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            [card.to_JSON(), overdraft.to_JSON()],
        )

    def test_timeline_with_credit_card(self):
        Income.objects.create(
            name='Job',
            user=self.user,
            amount=200,
            pay_type=PayType.MONTHLY,
        )
        CreditCard.objects.create(
            name='One',
            interest_rate=20.0,
            balance=1000,
            min_payment=10,
            min_payment_percent=10.0,
            annual_fee=100,
            user=self.user,
        )
        url = reverse('get-timeline')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['num_months'], 7)

    def test_timeline_with_credit_card_and_overdraft(self):
        Income.objects.create(
            name='Job',
            user=self.user,
            amount=100,
            pay_type=PayType.SEMI_MONTHLY,
        )
        CreditCard.objects.create(
            name='One',
            interest_rate=20.0,
            balance=1000,
            min_payment=10, 
            min_payment_percent=10.0,
            annual_fee=100,
            user=self.user,
        )
        overdraft = Overdraft.objects.create(
            name='Over',
            interest_rate=20.0,
            balance=1000,
            monthly_fee=9,
            user=self.user,
        )
        url = reverse('get-timeline')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['num_months'], 8)
