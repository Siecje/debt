from django.contrib.auth import get_user_model
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import (
    CreditCard,
    Expense,
    Income,
    Investment,
    Overdraft,
    TaxBracket,
    Type,
    User,
)
from .serializers import (
    CreateUserSerializer,
    CreditCardSerializer,
    DisplayExpenseSerializer,
    ExpenseSerializer,
    IncomeSerializer,
    InvestmentSerializer,
    OverdraftSerializer,
    TaxBracketSerializer,
    TypeSerializer,
    UserSerializer,
)
from .utils import sort_debts


@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'credit-cards': reverse('creditcard-list', request=request, format=format),
        'expenses': reverse('expense-list', request=request, format=format),
        'incomes': reverse('income-list', request=request, format=format),
        'overdrafts': reverse('overdraft-list', request=request, format=format),
        'types': reverse('type-list', request=request, format=format),
        'investments': reverse('investment-list', request=request, format=format),
        'tax-brackets': reverse('taxbracket-list', request=request, format=format),
        'auth-token': reverse('auth-token', request=request, format=format)
    })


class IsOwnerFilterBackend(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(user=request.user)


class CreditCardViewSet(viewsets.ModelViewSet):
    queryset = CreditCard.objects.all()
    serializer_class = CreditCardSerializer
    filter_backends = (IsOwnerFilterBackend,)
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'pk'


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    filter_backends = (IsOwnerFilterBackend,)
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'pk'

    def get_serializer_class(self):
        if self.request.method == 'GET':
            # Displays type.name
            return DisplayExpenseSerializer
        return ExpenseSerializer


class IncomeViewSet(viewsets.ModelViewSet):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    filter_backends = (IsOwnerFilterBackend,)
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'pk'


class OverdraftViewSet(viewsets.ModelViewSet):
    queryset = Overdraft.objects.all()
    serializer_class = OverdraftSerializer
    filter_backends = (IsOwnerFilterBackend,)
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'pk'


class TypeViewSet(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
    filter_backends = (IsOwnerFilterBackend,)
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'pk'


class InvestmentViewSet(viewsets.ModelViewSet):
    queryset = Investment.objects.all()
    serializer_class = InvestmentSerializer
    filter_backends = (IsOwnerFilterBackend,)
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'pk'


class TaxBracketViewSet(viewsets.ModelViewSet):
    queryset = TaxBracket.objects.all()
    serializer_class = TaxBracketSerializer
    filter_backends = (IsOwnerFilterBackend,)
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'pk'


class IsAdminOrOwner(permissions.BasePermission):
    """
    Object-level permission to allow admins or the user of an object to access it.
    Assumes the model instance has an `user` attribute.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        # Instance must have an attribute named `user`.
        return obj == request.user


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrOwner,)

    @action(methods=['POST'], detail=False)
    def create_user(self, request):
        serialized = CreateUserSerializer(data=request.data)
        if serialized.is_valid():
            user = get_user_model().objects.create_user(
                serialized.data.get('username'),
                email=serialized.data.get('email'),
                password=serialized.data.get('password'),
            )

            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return User.objects.none()
        elif self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.filter(pk=self.request.user.pk)


@api_view(['GET'])
def get_debts(request):
    """
    Though the annual fee with for a credit card will not go away
    when the debt is paid, the card should be cancelled so you can pay off
    other debt sooner.
    """
    overdrafts = Overdraft.objects.filter(user=request.user).order_by('monthly_fee').all()
    credit_cards = CreditCard.objects.order_by('interest_rate', 'annual_fee').all()
    result = sort_debts(list(overdrafts) + list(credit_cards))

    serialized = []
    for debt in result:
        serialized.append(debt.to_JSON())
    return Response(serialized)


@api_view(['GET'])
def get_debt_timeline(request):
    overdrafts = Overdraft.objects.filter(user=request.user).order_by('monthly_fee').all()
    credit_cards = CreditCard.objects.order_by('interest_rate', 'annual_fee').all()
    debts = sort_debts(list(overdrafts) + list(credit_cards))

    num_months = 0
    user = User.objects.get(username=request.user.username)
    # Amount to put towards debts
    payment = user.get_money_after_expenses()
    # Amount of debt each month
    debt_per_month = []

    for index, debt in enumerate(debts):
        result = debt.timeline(payment)
        if result['num_months'] == -1:
            return Response({'num_months': -1})
        # The current debt has been eliminated
        num_months += result['num_months']
        # Total debt each month for current debt
        debt_per_month = result['debt_per_month']
        if hasattr(debt, 'min_payment'):
            payment += debt.min_payment
        for debt in debts[index:]:
            # Need to add the debt owing on each of the other debts
            # minus the minimum payment for each month
            for month in debt_per_month:
                if hasattr(debt, 'min_payment'):
                    month += debt.balance + debt.cost() - debt.min_payment
                else:
                    month += debt.balance + debt.cost()

    return Response({
        'num_months': num_months,
        'debt_per_month': debt_per_month
    })
