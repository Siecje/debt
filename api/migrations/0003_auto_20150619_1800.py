# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_investment_taxbracket'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creditcard',
            name='user',
            field=models.ForeignKey(related_name='credit_cards', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='expense',
            name='user',
            field=models.ForeignKey(related_name='expenses', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='income',
            name='user',
            field=models.ForeignKey(related_name='incomes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='investment',
            name='user',
            field=models.ForeignKey(related_name='investments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='overdraft',
            name='user',
            field=models.ForeignKey(related_name='overdrafts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='taxbracket',
            name='user',
            field=models.ForeignKey(related_name='tax_brackets', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='type',
            name='user',
            field=models.ForeignKey(related_name='types', to=settings.AUTH_USER_MODEL),
        ),
    ]
