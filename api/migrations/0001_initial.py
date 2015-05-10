# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.auth.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='CreditCard',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.TextField()),
                ('interest_rate', models.FloatField()),
                ('balance', models.IntegerField()),
                ('min_payment', models.IntegerField()),
                ('min_payment_percent', models.FloatField()),
                ('annual_fee', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.TextField()),
                ('amount', models.IntegerField()),
                ('frequency', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.TextField()),
                ('amount', models.IntegerField()),
                ('frequency', models.IntegerField()),
                ('date', models.DateField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Overdraft',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.TextField()),
                ('balance', models.IntegerField()),
                ('monthly_fee', models.IntegerField()),
                ('interest_rate', models.FloatField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('auth.user',),
            managers=[
                (b'objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='type',
            name='user',
            field=models.ForeignKey(related_name='types', to='api.User'),
        ),
        migrations.AddField(
            model_name='overdraft',
            name='user',
            field=models.ForeignKey(related_name='overdrafts', to='api.User'),
        ),
        migrations.AddField(
            model_name='income',
            name='user',
            field=models.ForeignKey(related_name='incomes', to='api.User'),
        ),
        migrations.AddField(
            model_name='expense',
            name='type',
            field=models.ForeignKey(related_name='expenses', to='api.Type'),
        ),
        migrations.AddField(
            model_name='expense',
            name='user',
            field=models.ForeignKey(related_name='expenses', to='api.User'),
        ),
        migrations.AddField(
            model_name='creditcard',
            name='user',
            field=models.ForeignKey(related_name='credit_cards', to='api.User'),
        ),
    ]
