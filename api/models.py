import uuid
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models


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
    owed = models.IntegerField()
    min_payment = models.IntegerField()
    min_payment_percent = models.FloatField()
    annual_fee = models.IntegerField()

    user = models.ForeignKey(User, related_name='credit_cards')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('credit-card-detail', kwargs={'id': self.id})


class Overdraft(Common):
    name = models.TextField()
    owed = models.IntegerField()
    monthly_fee = models.IntegerField()

    user = models.ForeignKey(User, related_name='overdrafts')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('overdraft-detail', kwargs={'id': self.id})


from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
