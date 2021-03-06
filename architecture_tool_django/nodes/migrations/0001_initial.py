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
            name='Edge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('edge_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='edges', to='modeling.Edgetype')),
            ],
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('key', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('attributeSet', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('nodetype', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nodes', to='modeling.Nodetype')),
                ('target_nodes', models.ManyToManyField(related_name='source_nodes', through='nodes.Edge', to='nodes.Node')),
            ],
        ),
        migrations.AddField(
            model_name='edge',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outbound_edges', to='nodes.Node'),
        ),
        migrations.AddField(
            model_name='edge',
            name='target',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inbound_edges', to='nodes.Node'),
        ),
        migrations.AddConstraint(
            model_name='edge',
            constraint=models.UniqueConstraint(fields=('source', 'edge_type', 'target'), name='unique_edge'),
        ),
    ]
