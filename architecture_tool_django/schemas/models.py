from django.contrib.postgres.fields import JSONField
from django.db import models


class Schema(models.Model):
    key = models.CharField(max_length=50, primary_key=True)
    schema = JSONField()

    def __str__(self):
        return self.key
