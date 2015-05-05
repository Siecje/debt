from django.contrib.auth.models import User
from rest_framework import filters, permissions, serializers, viewsets
from rest_framework.decorators import api_view, list_route
from rest_framework.renderers import JSONRenderer
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
    lookup_field = 'id'


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    filter_backends = (IsOwnerFilterBackend,)
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'id'


class IncomeViewSet(viewsets.ModelViewSet):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    filter_backends = (IsOwnerFilterBackend,)
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'id'


class OverdraftViewSet(viewsets.ModelViewSet):
    queryset = Overdraft.objects.all()
    serializer_class = OverdraftSerializer
    filter_backends = (IsOwnerFilterBackend,)
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'id'


class TypeViewSet(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
    filter_backends = (IsOwnerFilterBackend,)
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'id'


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
    # queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrOwner,)

    @list_route(methods=['post'])
    def create_user(self, request):
        serialized = UserSerializer(data=request.DATA)
        if serialized.is_valid():
            User.objects.create_user(
                email=serialized.init_data['email'],
                username=serialized.init_data['username'],
                password=serialized.init_data['password']
            )
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        if self.request.user.is_anonymous():
            return User.objects.none()
        elif self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.filter(pk=self.request.user.pk)


@api_view(['GET'])
def get_debts(request):
    overdrafts = Overdraft.objects.filter(user=request.user).order_by('monthly_fee').all()
    credit_cards = CreditCard.objects.order_by('interest_rate', 'annual_fee').all()
    serialized = OverdraftSerializer(overdrafts, many=True).data + CreditCardSerializer(credit_cards, many=True).data
    return Response(serialized)
