from django.contrib.postgres.fields import JSONField
from django.db import models


class Node(models.Model):
    # STATUS_CHOICES = (
    #     ('DEFINED', 'Defined'),
    #     ('PLANNED', 'Planned'),
    #     ('IN DEVELOPMENT', 'In_development'),
    #     ('IN EVALUATION')
    #     ('BETA', 'Beta'),
    #     ('CALCELED', 'Canceled'),
    #     ('ACTIVE', 'Active'),
    #     ('DEPRECATED', 'Deprecated'),
    #     ('OUT_OF_SUPPORT', 'Out_of_support'),
    #     ('RETIRED', 'Retired'),
    # )
    key = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    status = models.CharField(
        max_length=50,
        blank=True,
        null=True
        #   choices=STATUS_CHOICES,
    )
    attributeSet = JSONField()

    def __str__(self):
        return f"{self.key}({self.name})"


class Edge(models.Model):
    node = models.ForeignKey(Node, on_delete=models.CASCADE, related_name="edges")
    type = models.CharField(max_length=50)
    target = models.CharField(max_length=50, db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["node", "type", "target"], name="unique_edge"
            )
        ]

    def __str__(self):
        return f"{self.node} -> {self.target} : {self.type}"
