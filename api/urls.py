from django.urls import include, path
from rest_framework.authtoken import views as auth_views
from rest_framework.urlpatterns import format_suffix_patterns

from . import views


creditcard_list = views.CreditCardViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

creditcard_detail = views.CreditCardViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

expense_list = views.ExpenseViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

expense_detail = views.ExpenseViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

income_list = views.IncomeViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

income_detail = views.IncomeViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

overdraft_list = views.OverdraftViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

overdraft_detail = views.OverdraftViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

type_list = views.TypeViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

type_detail = views.TypeViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

investment_list = views.InvestmentViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

investment_detail = views.InvestmentViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

taxbracket_list = views.TaxBracketViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

taxbracket_detail = views.TaxBracketViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

user_list = views.UserViewSet.as_view({
    'get': 'list',
    'post': 'create_user'
})

user_detail = views.UserViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

# urlpatterns = format_suffix_patterns([
urlpatterns = [
    path('', views.api_root, name='api-root'),
    path('credit-cards/',
        creditcard_list,
        name='creditcard-list'),
    path('credit-cards/<uuid:pk>/',
         creditcard_detail,
         name='creditcard-detail'),
    path('expenses/',
        expense_list,
        name='expense-list'),
    path('expenses/<uuid:pk>/',
         expense_detail,
         name='expense-detail'),
    path('incomes/',
        income_list,
        name='income-list'),
    path('incomes/<uuid:pk>/',
         income_detail,
         name='income-detail'),
    path('overdrafts/',
        overdraft_list,
        name='overdraft-list'),
    path('overdrafts/<uuid:pk>/',
        overdraft_detail,
        name='overdraft-detail'),
    path('types/',
        type_list,
        name='type-list'),
    path('types/<uuid:pk>/',
        type_detail,
        name='type-detail'),
    path('investments/',
        investment_list,
        name='investment-list'),
    path('investments/<uuid:pk>/',
        investment_detail,
        name='investment-detail'),
    path('taxbrackets/',
        taxbracket_list,
        name='taxbracket-list'),
    path('taxbrackets/<uuid:pk>/',
        taxbracket_detail,
        name='taxbracket-detail'),
    path('users/',
        user_list,
        name='user-list'),
    path('users/<int:pk>/',
        user_detail,
        name='user-detail'),
    path('debts/',
        views.get_debts,
        name='get-debts'),
    path('timeline/',
        views.get_debt_timeline,
        name='get-timeline')
]

urlpatterns += [
    path('auth/token/', auth_views.obtain_auth_token, name='auth-token'),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
]
