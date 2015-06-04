# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Investment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.TextField()),
                ('interest_rate', models.FloatField()),
                ('min_duration', models.IntegerField()),
                ('balance', models.IntegerField()),
                ('user', models.ForeignKey(related_name='investments', to='api.User')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TaxBracket',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('lower', models.IntegerField()),
                ('upper', models.IntegerField()),
                ('tax_rate', models.FloatField()),
                ('group', models.TextField()),
                ('user', models.ForeignKey(related_name='tax_brackets', to='api.User')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
