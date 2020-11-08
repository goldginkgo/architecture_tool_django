from collections import OrderedDict

import jsonschema
from django.db.models import Q
from jsonschema import Draft4Validator
from rest_framework import serializers

from architecture_tool_django.modeling.models import Edgetype, Nodetype

from ..models import Edge, Node


class EdgeSerializer(serializers.ModelSerializer):
    edge_type = serializers.CharField(source="edge_type.edgetype")

    class Meta:
        model = Edge
        fields = ["edge_type", "target"]

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # Here we filter the null values and creates a new dictionary
        # We use OrderedDict like in original method
        return OrderedDict([(key, ret[key]) for key in ret if ret[key] is not None])


class NodeSerializer(serializers.ModelSerializer):
    outbound_edges = EdgeSerializer(many=True, read_only=True)

    class Meta:
        model = Node
        fields = ["key", "nodetype", "attributeSet", "outbound_edges"]

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # Here we filter the null values and creates a new dictionary
        # We use OrderedDict like in original method
        return OrderedDict([(key, ret[key]) for key in ret if ret[key] is not None])

    def validate_attributeSet(self, value):
        nodetype = self.get_initial().get("nodetype")
        v = Draft4Validator(
            Nodetype.objects.get(pk=nodetype).attribute_schema.schema,
            format_checker=jsonschema.FormatChecker(),
        )
        errors = []
        for error in v.iter_errors(value):
            errors.append(error.message)

        if errors:
            raise serializers.ValidationError(errors)

        return value

    # def validate_outbound_edges(self, value):
    #     return value

    def create(self, validated_data):
        try:
            node = Node.objects.create(**validated_data)

            for edge in self.initial_data["outbound_edges"]:
                target_node = Node.objects.get(key=edge["target"])
                edge_type = Edgetype.objects.get(
                    Q(source_nodetype=node.nodetype)
                    & Q(target_nodetype=target_node.nodetype)
                    & Q(edgetype=edge["edge_type"])
                )
                node.add_edge(target_node, edge_type)

            node.save()
        except Exception as error:
            raise serializers.ValidationError(error)

        return node

    def update(self, instance, validated_data):
        try:
            instance.remove_all_edges()
            for edge in self.initial_data["outbound_edges"]:
                target_node = Node.objects.get(key=edge["target"])
                edge_type = Edgetype.objects.get(
                    Q(source_nodetype=instance.nodetype)
                    & Q(target_nodetype=target_node.nodetype)
                    & Q(edgetype=edge["edge_type"])
                )
                instance.add_edge(target_node, edge_type)

            instance.attributeSet = validated_data.get(
                "attributeSet", instance.attributeSet
            )
            instance.save()
        except Exception as error:
            raise serializers.ValidationError(error)

        return instance
