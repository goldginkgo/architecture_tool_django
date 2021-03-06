# Generated by Django 3.0.10 on 2020-10-14 14:16

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('modeling', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='List',
            fields=[
                ('key', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('listdef', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('schema', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lists', to='modeling.Schema')),
            ],
        ),
    ]
