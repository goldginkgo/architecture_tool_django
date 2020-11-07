from collections import OrderedDict

from jsonschema import Draft4Validator
from rest_framework import serializers

from ..models import Schema


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
