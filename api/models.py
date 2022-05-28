import json
import uuid

from django.conf import settings
from django.contrib.auth.models import User as AuthUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token


class User(AuthUser):

    class Meta:
        proxy = True

    def get_total_monthly_income(self):
        return sum([income.get_monthly_amount() for income in self.incomes.all()])

    def get_expenses(self):
        return sum([expense.amount for expense in self.expenses.all()])

    def get_minimum_payments(self):
        return sum([credit_card.min_payment for credit_card in self.credit_cards.all()])

    def get_total_debt(self):
        return (sum([credit_card.balance for credit_card in self.credit_cards.all()])
                + sum([overdraft.balance for overdraft in self.overdrafts.all()]))

    def get_money_after_expenses(self):
        # monthly
        return self.get_total_monthly_income() - self.get_expenses() - self.get_minimum_payments()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Common(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class DayOfWeek(models.IntegerChoices):
    SUNDAY = 0, _("Sunday")
    MONDAY = 1, _("Monday")
    TUESDAY = 2, _("Tuesday")
    WEDNESDAY = 3, _("Wednesday")
    THURSDAY = 4, _("Thursday")
    FRIDAY = 5, _("Friday")
    SATURDAY = 6, _("Saturday")


class PayType(models.IntegerChoices):
    WEEKLY = 0, _("weekly")
    BIWEEKLY = 1, _("biweekly")
    SEMI_MONTHLY = 2, _("semi-monthly")
    MONTHLY = 3, _("monthly")
    THIRTEEN_PAYS = 4, _("13 pay periods a year")


class Income(Common):
    name = models.TextField()
    pay_amount = models.IntegerField()
    # The day of the week you are paid
    # NULL for semi-monthly & monthly
    # semi-monthly means paid on 15th & last business day of the month
    # monthly means paid on the last business day of the month
    pay_day = models.IntegerField(choices=DayOfWeek.choices, null=True, blank=True)
    pay_type = models.IntegerField(choices=PayType.choices)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='incomes',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('income-detail', kwargs={'pk': self.id})

    def get_monthly_amount(self):
        if self.pay_type == PayType.WEEKLY:
            return self.pay_amount * (52 / 12)
        if self.pay_type == PayType.BIWEEKLY:
            return self.pay_amount * (52 / 2 / 12)
        if self.pay_type == PayType.SEMI_MONTHLY:
            return self.pay_amount * 2
        if self.pay_type == PayType.MONTHLY:
            return self.pay_amount
        # self.pay_type == PayType.THIRTEEN_PAYS:
        # TODO: what to do about THIRTEEN_PAYS?
        return self.pay_amount


class Type(Common):
    name = models.TextField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='types',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('type-detail', kwargs={'pk': self.id})


class Expense(Common):
    name = models.TextField()
    amount = models.IntegerField()
    frequency = models.IntegerField(default=0)

    type = models.ForeignKey(
        Type,
        related_name='expenses',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='expenses',
        on_delete=models.CASCADE,
    )


class CreditCard(Common):
    name = models.TextField()
    interest_rate = models.FloatField()
    balance = models.IntegerField()
    min_payment = models.IntegerField()
    min_payment_percent = models.FloatField()
    annual_fee = models.IntegerField()

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='credit_cards',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('credit-card-detail', kwargs={'pk': self.id})

    def to_JSON(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'interest_rate': self.interest_rate,
            'balance': self.balance,
            'min_payment': self.min_payment,
            'min_payment_percent': self.min_payment_percent,
            'annual_fee': self.annual_fee,
            'type': 'credit-card'
        }

    def cost(self):
        """ Amount that it is costing each month """
        return self.balance * (self.interest_rate / (100 * 12)) + self.annual_fee / float(12)

    def timeline(self, monthly_payment=None):
        """ Given a monthly payment how long will it take to pay off """
        amount = self.balance
        interest = 0
        points = []
        total_paid = 0
        total_interest = 0

        while amount > 0:
            interest = amount * (self.interest_rate / 100 / 12)
            total_interest += interest
            amount += interest
            if len(points) % 12 == 0:
                amount += self.annual_fee
            payment = monthly_payment or amount * self.min_payment_percent

            if payment < self.min_payment:
                payment = self.min_payment

            if payment > amount:
                payment = amount

            total_paid += payment
            amount -= payment
            points.append(amount)

        return {
            'debt_per_month': points,
            'num_months': len(points),
            'total_interest_paid': total_interest,
            'total_paid': total_paid
        }


class Overdraft(Common):
    name = models.TextField()
    balance = models.IntegerField()
    monthly_fee = models.IntegerField()
    interest_rate = models.FloatField()

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='overdrafts',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('overdraft-detail', kwargs={'pk': self.id})

    def to_JSON(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'interest_rate': self.interest_rate,
            'balance': self.balance,
            'monthly_fee': self.monthly_fee,
            'type': 'overdraft'
        }

    def cost(self):
        """ Amount that it is costing each month """
        return self.balance * (self.interest_rate / (100 * 12)) + self.monthly_fee

    def timeline(self, monthly_payment):
        """ Given a monthly payment how long will it take to pay off """
        amount = self.balance
        interest = 0
        points = []
        total_paid = 0
        total_interest = 0

        previous_amount = amount

        while amount > 0:
            interest = amount * (self.interest_rate / 100)
            total_interest += interest
            amount += interest
            amount += self.monthly_fee
            payment = monthly_payment

            if payment > amount:
                payment = amount

            total_paid += payment
            amount -= payment
            points.append(amount)
            if amount > previous_amount:
                break

        return {
            'debt_per_month': points,
            'num_months': len(points),
            'total_interest_paid': total_interest,
            'total_paid': total_paid
        }


class Investment(Common):
    name = models.TextField()
    interest_rate = models.FloatField()
    # min_duration is in months
    # 0 means you can access it at any time
    min_duration = models.IntegerField()
    balance = models.IntegerField()

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='investments',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class TaxBracket(Common):
    lower = models.IntegerField()
    upper = models.IntegerField()
    tax_rate = models.FloatField()
    # group is used for displaying tax brackets together
    # for example federal vs provincial
    group = models.TextField()

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='tax_brackets',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return '{0}% {1} - {2}'.format(self.tax_rate, self.lower, self.upper)

    def clean(self):
        if self.upper != 0 and self.upper < self.lower:
            raise ValidationError('The upper bound must be larger than the lower bound.')
