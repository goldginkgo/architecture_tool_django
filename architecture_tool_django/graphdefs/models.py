from django.contrib.postgres.fields import JSONField
from django.db import models

from architecture_tool_django.modeling.models import Schema


class Graph(models.Model):
    key = models.CharField(max_length=50, primary_key=True)
    schema = models.ForeignKey(
        Schema, on_delete=models.SET_NULL, null=True, related_name="graphs"
    )
    validation_error = models.BooleanField(default=False)
    graph = JSONField(default=dict)

    def __str__(self):
        return self.key
