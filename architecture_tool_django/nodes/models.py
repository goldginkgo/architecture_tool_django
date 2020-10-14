from django.contrib.postgres.fields import JSONField
from django.db import models

from architecture_tool_django.modeling.models import Edgetype, Nodetype


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
    nodetype = models.ForeignKey(
        Nodetype, on_delete=models.CASCADE, related_name="nodes"
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    attributeSet = JSONField(default=dict)
    target_nodes = models.ManyToManyField(
        "self", through="Edge", symmetrical=False, related_name="source_nodes"
    )

    def __str__(self):
        if ("name" in self.attributeSet) and self.attributeSet["name"]:
            return f"{self.key} ({self.attributeSet['name']})"
        else:
            return self.key

    def add_edge(self, node, edge_type):
        edge, created = Edge.objects.get_or_create(
            source=self, target=node, edge_type=edge_type
        )
        return edge

    def remove_edge(self, node, edge_type):
        Edge.objects.filter(source=self, target=node, edge_type=edge_type).delete()
        return

    def remove_all_edges(self):
        Edge.objects.filter(source=self).delete()
        return

    def get_target_nodes_with_edgetype(self, edge_type):
        return self.related_nodes.filter(
            inbound_edges__edge_type=edge_type, inbound_edges__source=self
        )

    def get_source_nodes_with_edgetype(self, edge_type):
        return self.related_to.filter(
            outbound_edges__edge_type=edge_type, outbound_edges__target=self
        )


class Edge(models.Model):
    source = models.ForeignKey(
        Node, on_delete=models.CASCADE, related_name="outbound_edges"
    )
    target = models.ForeignKey(
        Node, on_delete=models.CASCADE, related_name="inbound_edges"
    )
    edge_type = models.ForeignKey(
        Edgetype, on_delete=models.CASCADE, related_name="edges"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["source", "edge_type", "target"], name="unique_edge"
            )
        ]

    def __str__(self):
        return f"{self.source} -> {self.target} : {self.edge_type}"
