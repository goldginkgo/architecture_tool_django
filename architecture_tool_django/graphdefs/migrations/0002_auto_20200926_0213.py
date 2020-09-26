# Generated by Django 3.0.10 on 2020-09-26 02:13

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('graphdefs', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='graph',
            name='consumers',
        ),
        migrations.RemoveField(
            model_name='graph',
            name='description',
        ),
        migrations.RemoveField(
            model_name='graph',
            name='edges',
        ),
        migrations.RemoveField(
            model_name='graph',
            name='nodes',
        ),
        migrations.RemoveField(
            model_name='graph',
            name='status',
        ),
        migrations.RemoveField(
            model_name='graph',
            name='title',
        ),
        migrations.RemoveField(
            model_name='graph',
            name='value',
        ),
        migrations.AddField(
            model_name='graph',
            name='graph',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict),
        ),
    ]
