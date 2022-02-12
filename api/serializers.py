from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import CreditCard, Expense, Income, Investment, \
                    Overdraft, TaxBracket, Type


class RelatedUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'url')
        lookup_field = 'pk'


class RelatedExpenseSerializer(serializers.HyperlinkedModelSerializer):
    user = RelatedUserSerializer(
        read_only=True
    )

    class Meta:
        model = Expense
        fields = ('id', 'name', 'amount', 'frequency', 'user')
        lookup_field = 'pk'


class RelatedTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Type
        fields = ('id', 'url', 'name')
        lookup_field = 'pk'


class IncomeSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Income
        fields = ('id', 'name', 'amount', 'frequency', 'date', 'user', 'created', 'updated')


class TypeSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    expenses = RelatedExpenseSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Type
        fields = ('id', 'name', 'user', 'expenses', 'created', 'updated')


class DisplayExpenseSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    type = RelatedTypeSerializer()

    class Meta:
        model = Expense
        fields = ('id', 'name', 'amount', 'frequency', 'type', 'user', 'created', 'updated')


class ExpenseSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Expense
        fields = ('id', 'name', 'amount', 'frequency', 'type', 'user', 'created', 'updated')


class CreditCardSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = CreditCard
        fields = ('id', 'name', 'interest_rate', 'balance', 'min_payment',
                  'min_payment_percent', 'annual_fee', 'user')


class OverdraftSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Overdraft
        fields = ('id', 'name', 'balance', 'monthly_fee', 'interest_rate', 'user')


class InvestmentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Investment
        fields = ('id', 'name', 'interest_rate', 'min_duration', 'balance', 'user')


class TaxBracketSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = TaxBracket
        fields = ('id', 'lower', 'upper', 'tax_rate', 'group', 'user')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('username', 'email')


class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password')
