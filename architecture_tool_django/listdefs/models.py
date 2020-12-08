from django.contrib.postgres.fields import JSONField
from django.db import models

from architecture_tool_django.modeling.models import Schema


class List(models.Model):
    key = models.CharField(max_length=50, primary_key=True)
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE, related_name="lists")
    validation_error = models.BooleanField(default=False)
    listdef = JSONField(default=dict)

    def __str__(self):
        return self.key

    def save(self, *args, **kwargs):
        validation = kwargs.pop("schema_validation_task", None)
        if not validation:  # if it's not comming from the schema validation task
            self.validation_error = False
        super(List, self).save(*args, **kwargs)
