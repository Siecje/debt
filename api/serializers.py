from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import (
    CreditCard,
    DayOfWeek,
    Expense,
    Income,
    Investment,
    Overdraft,
    PayType,
    TaxBracket,
    Type,
)


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
    url = serializers.SerializerMethodField()

    class Meta:
        model = Type
        fields = ('id', 'url', 'name')
        lookup_field = 'pk'

    def get_url(self, obj):
        return obj.get_absolute_url()


class PayDayField(serializers.ChoiceField):
    def to_representation(self, value):
        if not value:
            return value
        return DayOfWeek.labels[value]

    def to_internal_value(self, value):
        if not value:
            return value
        inverted = {v: k for k, v in self.choices.items()}
        return inverted[value]


class PayTypeField(serializers.ChoiceField):
    def to_representation(self, value):
        if not value:
            return value
        return PayType.labels[value]

    def to_internal_value(self, value):
        if not value:
            return value
        inverted = {v: k for k, v in self.choices.items()}
        return inverted[value]


class IncomeSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    pay_day = PayDayField(choices=DayOfWeek.choices, required=False)
    pay_type = PayTypeField(choices=PayType.choices)
    monthly_amount = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = Income
        fields = (
            'id',
            'monthly_amount',
            'name',
            'pay_amount',
            'pay_day',
            'pay_type',
            'url',
            'user',
            'date_created',
            'date_updated',
        )

    def get_monthly_amount(self, obj):
        return obj.get_monthly_amount()

    def get_url(self, obj):
        return obj.get_absolute_url()


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
        fields = ('id', 'name', 'user', 'expenses', 'date_created', 'date_updated')


class DisplayExpenseSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    type = RelatedTypeSerializer()

    class Meta:
        model = Expense
        fields = ('id', 'name', 'amount', 'frequency', 'type', 'user', 'date_created', 'date_updated')


class ExpenseSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Expense
        fields = ('id', 'name', 'amount', 'frequency', 'type', 'user', 'date_created', 'date_updated')


class CreditCardSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    url = serializers.SerializerMethodField()

    class Meta:
        model = CreditCard
        fields = ('id', 'name', 'interest_rate', 'balance', 'min_payment',
                  'min_payment_percent', 'annual_fee', 'url', 'user')

    def get_url(self, obj):
        return obj.get_absolute_url()


class OverdraftSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Overdraft
        fields = ('id', 'name', 'balance', 'monthly_fee', 'interest_rate', 'url', 'user')

    def get_url(self, obj):
        return obj.get_absolute_url()

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

    def validate(self, data):
        if data['upper'] != 0 and data['lower'] > data['upper']:
            raise serializers.ValidationError('The upper bound must be larger than the lower bound.')
        return data


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('username', 'email')


class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password')
