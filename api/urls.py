from django.conf.urls import include, url
from django.contrib import admin
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

urlpatterns = format_suffix_patterns([
    url(r'^$', views.api_root),
    url(r'^credit-cards/?$',
        creditcard_list,
        name='creditcard-list'),
    url(r'^credit-cards/(?P<id>[^/]+)/?$',
         creditcard_detail,
         name='creditcard-detail'),
    url(r'^expenses/?$',
        expense_list,
        name='expense-list'),
    url(r'^expenses/(?P<id>[^/]+)/?$',
         expense_detail,
         name='expense-detail'),
    url(r'^incomes/?$',
        income_list,
        name='income-list'),
    url(r'^incomes/(?P<id>[^/]+)/?$',
         income_detail,
         name='income-detail'),
    url(r'^overdrafts/?$',
        overdraft_list,
        name='overdraft-list'),
    url(r'^overdrafts/(?P<id>[^/]+)/?$',
        overdraft_detail,
        name='overdraft-detail'),
    url(r'^types/?$',
        type_list,
        name='type-list'),
    url(r'^types/(?P<id>[^/]+)/?$',
        type_detail,
        name='type-detail'),
    url(r'^users/?$',
        user_list,
        name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/?$',
        user_detail,
        name='user-detail'),
    url(r'^debts/?$',
        views.get_debts,
        name='get-debts'),
    url(r'^timeline/?$',
        views.get_debt_timeline,
        name='get-timeline')
])

urlpatterns += [
    url(r'^auth/token/?$', auth_views.obtain_auth_token, name='auth-token'),
    url(r'^auth/', include('rest_framework.urls',
                           namespace='rest_framework')),
]
