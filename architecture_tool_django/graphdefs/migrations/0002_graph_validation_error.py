# Generated by Django 3.0.10 on 2020-11-18 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graphdefs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='graph',
            name='validation_error',
            field=models.BooleanField(default=False),
        ),
    ]