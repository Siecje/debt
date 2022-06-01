import json

from django.urls import reverse

from api.models import CreditCard, Income, Overdraft, PayType
from api.utils import serialize_money
from .base import APIBaseTest


class DebtTests(APIBaseTest):
    url = reverse('get-debts')

    def test_get_debts(self):
        credit_card = CreditCard.objects.create(
            name='First',
            interest_rate=20.0,
            balance=1000_00,
            min_payment=10_00,
            min_payment_percent=15.0,
            annual_fee=100_00,
            user=self.user,
        )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            [credit_card.to_JSON()],
        )

    def test_credit_cards_sorted_by_interest_rate(self):
        # The same for both
        balance = 1000_00
        min_payment = 10_00
        min_payment_percent = 10.0
        annual_fee = 100_00
        card1 = CreditCard.objects.create(
            name='One',
            interest_rate=20.0,
            balance=balance,
            min_payment=min_payment,
            min_payment_percent=min_payment_percent,
            annual_fee=annual_fee,
            user=self.user,
        )
        card2 = CreditCard.objects.create(
            name='Two',
            interest_rate=20.1,
            balance=balance,
            min_payment=min_payment,
            min_payment_percent=min_payment_percent,
            annual_fee=annual_fee,
            user=self.user,
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            [card2.to_JSON(), card1.to_JSON()],
        )
        self.assertEqual(self.user.get_total_debt(), serialize_money(balance + balance))

    def test_debts_sorted_by_fee(self):
        """
        Montly/Annual costs should be considered
        """
        card = CreditCard.objects.create(
            name='One',
            interest_rate=20.0,
            balance=1000_00,
            min_payment=10_00,
            min_payment_percent=10.0,
            annual_fee=100_00,
            user=self.user,
        )
        overdraft = Overdraft.objects.create(
            name='Over',
            interest_rate=20.0,
            balance=1000_00,
            monthly_fee=9_00,
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
            balance=1000_00,
            min_payment=10_00,
            min_payment_percent=10.0,
            annual_fee=111_00,
            user=self.user,
        )
        card2 = CreditCard.objects.create(
            name='Two',
            interest_rate=21.0,
            balance=1000_00,
            min_payment=10_00,
            min_payment_percent=10.0,
            annual_fee=100_00,
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
            balance=1000_00,
            min_payment=10_00,
            min_payment_percent=10.0,
            annual_fee=100_00,
            user=self.user,
        )
        overdraft = Overdraft.objects.create(
            name='Over',
            interest_rate=21.0,
            balance=1000_00,
            monthly_fee=5_00,
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
            pay_amount=200_00,
            pay_type=PayType.MONTHLY,
        )
        CreditCard.objects.create(
            name='One',
            interest_rate=20.0,
            balance=1000_00,
            min_payment=10_00,
            min_payment_percent=10.0,
            annual_fee=100_00,
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
            pay_amount=500_00,
            pay_type=PayType.SEMI_MONTHLY,
        )
        CreditCard.objects.create(
            name='One',
            interest_rate=20.0,
            balance=1000_00,
            min_payment=10_00,
            min_payment_percent=10.0,
            annual_fee=100_00,
            user=self.user,
        )
        Overdraft.objects.create(
            name='Over',
            interest_rate=20.0,
            balance=1000_00,
            monthly_fee=9_00,
            user=self.user,
        )
        url = reverse('get-timeline')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['num_months'], 4)

    def test_timeline_cannot_reduce_debt(self):
        Income.objects.create(
            name='Job',
            user=self.user,
            pay_amount=100_00,
            pay_type=PayType.SEMI_MONTHLY,
        )
        CreditCard.objects.create(
            name='One',
            interest_rate=20.0,
            balance=1000_00,
            min_payment=10_00,
            min_payment_percent=10.0,
            annual_fee=100_00,
            user=self.user,
        )
        Overdraft.objects.create(
            name='Over',
            interest_rate=20.0,
            balance=1000_00,
            monthly_fee=9_00,
            user=self.user,
        )
        url = reverse('get-timeline')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['num_months'], -1)
