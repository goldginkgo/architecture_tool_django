# Generated by Django 3.0.10 on 2020-10-03 11:34

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('modeling', '0005_auto_20201001_0230'),
        ('nodes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='edge',
            name='unique_edge',
        ),
        migrations.RemoveField(
            model_name='edge',
            name='node',
        ),
        migrations.RemoveField(
            model_name='edge',
            name='type',
        ),
        migrations.RemoveField(
            model_name='node',
            name='name',
        ),
        migrations.RemoveField(
            model_name='node',
            name='status',
        ),
        migrations.RemoveField(
            model_name='node',
            name='type',
        ),
        migrations.AddField(
            model_name='edge',
            name='edge_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='edges', to='modeling.Edgetype'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='edge',
            name='source',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='outbound_edges', to='nodes.Node'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='node',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='node',
            name='nodetype',
            field=models.ForeignKey(default=django.utils.timezone.now, on_delete=django.db.models.deletion.CASCADE, related_name='nodes', to='modeling.Nodetype'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='node',
            name='related_nodes',
            field=models.ManyToManyField(related_name='related_to', through='nodes.Edge', to='nodes.Node'),
        ),
        migrations.AddField(
            model_name='node',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='edge',
            name='target',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inbound_edges', to='nodes.Node'),
        ),
        migrations.AlterField(
            model_name='node',
            name='attributeSet',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict),
        ),
        migrations.AddConstraint(
            model_name='edge',
            constraint=models.UniqueConstraint(fields=('source', 'edge_type', 'target'), name='unique_edge'),
        ),
    ]