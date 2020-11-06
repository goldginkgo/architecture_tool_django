from django.contrib.postgres.fields import JSONField
from django.db import models


class Schema(models.Model):
    key = models.CharField(max_length=50, primary_key=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    schema = JSONField(default=dict)

    def __str__(self):
        return self.key


class Nodetype(models.Model):
    UMT_TYPE_CHOICES = [
        ("node", "node"),
        ("component", "component"),
        ("interface", "interface"),
        ("package", "package"),
        ("folder", "folder"),
        ("frame", "frame"),
        ("cloud", "cloud"),
        ("database", "database"),
    ]

    key = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, null=True)
    attribute_schema = models.ForeignKey(
        Schema, on_delete=models.CASCADE, related_name="nodetypes"
    )
    umlType = models.CharField(max_length=50, default="node", choices=UMT_TYPE_CHOICES)
    folder = models.CharField(max_length=50)
    target_nodetypes = models.ManyToManyField(
        "self", through="Edgetype", symmetrical=False, related_name="source_nodetypes"
    )

    def __str__(self):
        return self.name

    # def add_edgetype(self, nodetype, edgetype):
    #     edgetype, created = Edgetype.objects.get_or_create(
    #         source_nodetype=self, target_nodetype=nodetype, edgetype=edgetype
    #     )
    #     return edgetype

    # def remove_edgetype(self, nodetype, edgetype):
    #     Edgetype.objects.filter(source_nodetype=self, target_nodetype=nodetype, edgetype=edgetype).delete()
    #     return

    # def remove_all_edgetypes(self):
    #     Edgetype.objects.filter(source_nodetype=self).delete()
    #     return

    # def get_target_nodetypes_with_edgetype(self, edgetype):
    #     return self.target_nodes.filter(
    #         inbound_edgetypes__edgetype=edgetype, inbound_edgetypes__source_nodetype=self
    #     )

    # def get_source_nodetypes_with_edgetype(self, edge_type):
    #     return self.source_nodes.filter(
    #         outbound_edgetypes__edge_type=edge_type, outbound_edgetypes__target_nodetype=self
    #     )


class Edgetype(models.Model):
    source_nodetype = models.ForeignKey(
        Nodetype, on_delete=models.CASCADE, related_name="outbound_edgetypes"
    )
    target_nodetype = models.ForeignKey(
        Nodetype, on_delete=models.CASCADE, related_name="inbound_edgetypes"
    )
    edgetype = models.CharField(max_length=50)
    edgetype_name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["source_nodetype", "edgetype", "target_nodetype"],
                name="unique_edgetype",
            )
        ]

    def __str__(self):
        return self.edgetype
