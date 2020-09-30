from django.contrib.postgres.fields import JSONField
from django.db import models


class Nodetype(models.Model):
    key = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, null=True)
    umlType = models.CharField(max_length=50, blank=True, null=True)
    keyFormat = models.CharField(max_length=50, blank=True, null=True)
    inherits = models.CharField(max_length=50, blank=True, null=True)
    folder = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Edgetype(models.Model):
    key = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, null=True)
    # owner = models.CharField(max_length=100, blank=True, null=True)
    # purpose = models.CharField(max_length=255, blank=True, null=True)
    # inheritsPairs = models.CharField(max_length=50, null=True)
    # pairs = JSONField()

    def __str__(self):
        return self.key


class Schema(models.Model):
    key = models.CharField(max_length=50, primary_key=True)
    schema = JSONField(default=dict)

    def __str__(self):
        return self.key
