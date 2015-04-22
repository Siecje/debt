from django.contrib.auth.models import User
from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .models import CreditCard, Expense, Income, Overdraft, Type
from .serializers import CreditCardSerializer, ExpenseSerializer, \
                         IncomeSerializer, OverdraftSerializer, \
                         TypeSerializer, UserSerializer


@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'credit-cards': reverse('creditcard-list', request=request, format=format),
        'expenses': reverse('expense-list', request=request, format=format),
        'incomes': reverse('income-list', request=request, format=format),
        'overdrafts': reverse('overdraft-list', request=request, format=format),
        'types': reverse('type-list', request=request, format=format),
        # 'auth-token': reverse('rest_framework.authtoken.views.obtain_auth_token', request=request, format=format)
    })


class CreditCardViewSet(viewsets.ModelViewSet):
    queryset = CreditCard.objects.all()
    serializer_class = CreditCardSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    lookup_field = 'id'


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    lookup_field = 'id'


class IncomeViewSet(viewsets.ModelViewSet):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    lookup_field = 'id'


class OverdraftViewSet(viewsets.ModelViewSet):
    queryset = Overdraft.objects.all()
    serializer_class = OverdraftSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    lookup_field = 'id'


class TypeViewSet(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    lookup_field = 'id'


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
