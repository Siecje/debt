import uuid
from django.contrib.auth.models import User as AuthUser
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class User(AuthUser):
    class Meta:
        proxy = True

    def get_total_income(self):
        return sum([income.amount for income in self.incomes.all()])

    def get_expenses(self):
        return sum([expense.amount for expense in self.expenses.all()])

    def get_minimum_payments(self):
        return sum([credit_card.min_payment for credit_card in self.credit_cards.all()])

    def get_debt(self):
        return (sum([credit_card.balance for credit_card in self.credit_cards.all()])
                + sum([overdraft.balance for overdraft in self.overdrafts.all()]))

    def get_money_after_expenses(self):
        # monthly
        return self.get_total_income() - self.get_expenses() - self.get_minimum_payments()


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Common(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Income(Common):
    name = models.TextField()
    amount = models.IntegerField()
    # How often you receive self.amount
    frequency = models.IntegerField()
    # One of your pay days
    date = models.DateField()

    user = models.ForeignKey(User, related_name='incomes')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('income-detail', kwargs={'id': self.id})


class Type(Common):
    name = models.TextField()
    user = models.ForeignKey(User, related_name='types')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('type-detail', kwargs={'id': self.id})


class Expense(Common):
    name = models.TextField()
    amount = models.IntegerField()
    frequency = models.IntegerField(default=0)

    type = models.ForeignKey(Type, related_name='expenses')
    user = models.ForeignKey(User, related_name='expenses')


class CreditCard(Common):
    name = models.TextField()
    interest_rate = models.FloatField()
    balance = models.IntegerField()
    min_payment = models.IntegerField()
    min_payment_percent = models.FloatField()
    annual_fee = models.IntegerField()

    user = models.ForeignKey(User, related_name='credit_cards')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('credit-card-detail', kwargs={'id': self.id})

    def to_JSON(self):
        return {
            'id': self.id,
            'name': self.name,
            'interest_rate': self.interest_rate,
            'balance': self.balance,
            'min_payment': self.min_payment,
            'min_payment_percent': self.min_payment_percent,
            'annual_fee': self.annual_fee,
            'type': 'credit-card'
        }

    def cost(self):
        return self.balance * (self.interest_rate / 100) + self.annual_fee

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
            payment = monthly_payment or amount * self.min_payment_percent

            if payment < self.min_payment:
                payment = self.min_payment

            if payment > amount:
                payment = amount

            total_paid += payment
            amount -= payment
            points.append(amount)

        return {
            'months': len(points),
            'total_interest_paid': total_interest,
            'total_paid': total_paid
        }


class Overdraft(Common):
    name = models.TextField()
    balance = models.IntegerField()
    monthly_fee = models.IntegerField()
    interest_rate = models.FloatField()

    user = models.ForeignKey(User, related_name='overdrafts')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('overdraft-detail', kwargs={'id': self.id})

    def to_JSON(self):
        return {
            'id': self.id,
            'name': self.name,
            'interest_rate': self.interest_rate,
            'balance': self.balance,
            'monthly_fee': self.monthly_fee,
            'type': 'overdraft'
        }

    def cost(self):
        return self.balance * (self.interest_rate / 100) + self.monthly_fee * 12


class Investment(Common):
    name = models.TextField()
    interest_rate = models.FloatField()
    # min_duration is in months
    # 0 means you can access it at any time
    min_duration = models.IntegerField()
    balance = models.IntegerField()

    user = models.ForeignKey(User, related_name='investments')

    def __str__(self):
        return self.name


class TaxBracket(Common):
    lower = models.IntegerField()
    upper = models.IntegerField()
    tax_rate = models.FloatField()
    # group is used for displaying tax brackets together
    # for example federal vs provincial
    group = models.TextField()

    user = models.ForeignKey(User, related_name='tax_brackets')

    def __str__(self):
        return '%s %d - %d' % (self.tax_rate, self.lower, self.upper)

    def clean(self):
        if self.upper != 0 and self.upper < self.lower:
            raise ValidationError('The upper bound must be larger than the lower bound.')
