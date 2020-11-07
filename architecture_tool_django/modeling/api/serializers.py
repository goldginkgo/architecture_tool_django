from collections import OrderedDict

from jsonschema import Draft4Validator
from rest_framework import serializers

from ..models import Edgetype, Nodetype, Schema


class SchemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schema
        fields = ["key", "description", "schema"]

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # Here we filter the null values and creates a new dictionary
        # We use OrderedDict like in original method
        return OrderedDict([(key, ret[key]) for key in ret if ret[key] is not None])

    def validate_schema(self, value):
        """
        Validate if the shema conforms to JSON Schema specification.
        """
        try:
            Draft4Validator.check_schema(value)
        except Exception as err:
            raise serializers.ValidationError(err.message)

        return value


class NodetypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nodetype
        fields = ["key", "name", "description", "attribute_schema", "umlType", "folder"]

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # Here we filter the null values and creates a new dictionary
        # We use OrderedDict like in original method
        return OrderedDict([(key, ret[key]) for key in ret if ret[key] is not None])


class EdgetypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Edgetype
        fields = [
            "source_nodetype",
            "target_nodetype",
            "edgetype",
            "edgetype_name",
            "description",
        ]

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # Here we filter the null values and creates a new dictionary
        # We use OrderedDict like in original method
        return OrderedDict([(key, ret[key]) for key in ret if ret[key] is not None])
