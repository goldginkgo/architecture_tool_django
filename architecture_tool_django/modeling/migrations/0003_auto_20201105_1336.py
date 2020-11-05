# Generated by Django 3.0.10 on 2020-11-05 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modeling', '0002_auto_20201018_0111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nodetype',
            name='umlType',
            field=models.CharField(choices=[('node', 'node'), ('component', 'component'), ('interface', 'interface'), ('package', 'package'), ('folder', 'folder'), ('frame', 'frame'), ('cloud', 'cloud'), ('database', 'database')], default='node', max_length=50),
        ),
    ]
