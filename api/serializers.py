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
    class Meta:
        model = Type
        fields = ('id', 'url', 'name')
        lookup_field = 'pk'


class IncomeSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    pay_day = serializers.SerializerMethodField()
    # pay_type = serializers.SerializerMethodField()
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

    def get_pay_day(self, obj):
        # TODO: Use translation in DayOfWeek definition?
        day_as_string = {
            DayOfWeek.SUNDAY: 'Sunday',
            DayOfWeek.MONDAY: 'Monday',
            DayOfWeek.TUESDAY: 'Tuesday',
            DayOfWeek.WEDNESDAY: 'Wednesday',
            DayOfWeek.THURSDAY: 'Thursday',
            DayOfWeek.FRIDAY: 'Friday',
            DayOfWeek.SATURDAY: 'Saturday',
            None: None,
        }
        return day_as_string[obj.pay_day]
        
    def get_monthly_amount(self, obj):
        return obj.get_monthly_amount()

    def get_url(self, obj):
        return obj.get_absolute_url()

    # def get_pay_type(self, obj):
    #     pay_type_as_string = {
    #         PayType.WEEKLY: 'Weekly',
    #         PayType.BIWEEKLY: 'Bi-weekly',
    #         PayType.MONTHLY: 'Monthly',
    #         PayType.SEMI_MONTHLY: 'Semi Monthly',
    #         PayType.THIRTEEN_PAYS: 'Thirteen Pays',
    #     }
    #     return pay_type_as_string[obj.pay_type]




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
