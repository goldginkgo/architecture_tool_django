# Generated by Django 3.0.10 on 2020-09-25 05:54

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('modeling', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schema',
            name='schema',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]
