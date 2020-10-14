from django.contrib.postgres.fields import JSONField
from django.db import models

from architecture_tool_django.modeling.models import Schema


class List(models.Model):
    key = models.CharField(max_length=50, primary_key=True)
    schema = models.ForeignKey(
        Schema, on_delete=models.SET_NULL, null=True, related_name="lists"
    )
    # title = models.CharField(max_length=100)
    # description = models.CharField(max_length=255, blank=True, null=True)
    # value = models.CharField(max_length=255, blank=True, null=True)
    # consumers = models.CharField(max_length=255, blank=True, null=True)
    # status = models.CharField(max_length=50)
    listdef = JSONField(default=dict)

    def __str__(self):
        return self.key
